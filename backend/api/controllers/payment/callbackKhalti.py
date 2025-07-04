from api import db, mail
from flask_mail import Message
from flask import redirect, jsonify, render_template
from api.models.registration import Registration
from api.models.user import User
from api.models.event import Event
from firebase_admin import auth
from api.utils.logger import Logger
import os
import dotenv
import requests
import qrcode
import io
import base64
from email.utils import make_msgid
from cryptography.fernet import Fernet, InvalidToken
import json

dotenv.load_dotenv()

def CallbackKhalti(registration_id, payment_status, pidx):
    # validate request args
    if not registration_id or payment_status != "Completed":
        return {"message": "Payment status or registration id not valid"}, 400

    # cross check with khalti 
    try:
        response = requests.post(
            "https://dev.khalti.com/api/v2/epayment/lookup/",
            json={"pidx": pidx},
            headers={"Authorization": f"key {os.getenv('KHALTI_API_KEY')}"}
        )
        data = response.json()
        if data.get("status") != "Completed":
            raise ValueError(f"Payment status not completed: {data.get('status')}")
    except Exception as e:
        Logger.error(f"Error validating payment: {e}")
        return {"message": "Error validating Payment"}, 402

    # save in database
    try:
        registration = Registration.query.get(registration_id)
        if not registration:
            raise ValueError("Given registration not found")

        registration.payment_status = 'completed'
        db.session.add(registration)
        db.session.commit()
    except Exception as e:
        Logger.error(f"Error saving registration: {e}")
        return {"message": "Error saving registration"}, 500

    # prepare registration mail
    try:
        user = auth.get_user(registration.user_id)
        event = Event.query.get(registration.event_id)
    except Exception as e:
        Logger.error(f"Error fetching registered user or event: {e}")
        return {"message": "Error fetching event or user information"}, 500

    # Generate encrypted QR code as base64
    qr_data = {
        "registration_id": registration.registration_id,
        "user_id": registration.user_id,
        "user_name": user.display_name,
    }

    key = os.getenv("REGISTRATION_VERIFICATION_KEY")
    if not key:
        Logger.error("Registration verification key is not set in environment variables.")
        return {"message": "Internal server error"}, 500

    try:
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(json.dumps(qr_data).encode())
    except InvalidToken:
        Logger.error("Invalid token: encryption failed.")
        return {"message": "Internal server error"}, 400

    verification_url = f"{os.getenv('BACKEND_URL')}/api/registration/verifyRegistration?encryptedData={encrypted_data.decode()}"
    qr_img = qrcode.make(verification_url)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    cid = make_msgid(domain="example.com")[1:-1]
    image_bytes = buf.getvalue()

    # Prepare data for email
    registration_info = {
        "userName": user.display_name,
        "eventName": event.title,
        "RegistrationNumber": registration.registration_id,
        "Date": event.event_date.strftime("%Y-%m-%d"),
        "Time": event.event_date.strftime("%H:%M"),
        "userEmail": user.email,
        "location": event.location,
        "description": event.description,
        "qrCode": f"cid:{cid}",
    }

    # Compose email
    msg = Message(
        subject=f"You have registered for {event.title}",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[user.email],
    )
    msg.html = render_template("RegistrationTicket.html", **registration_info)
    msg.attach(
        filename="qrCode.png",
        content_type="image/png",
        data=image_bytes,
        headers={"Content-ID": f"<{cid}>"},
    )

    try:
        mail.send(msg)
    except Exception as e:
        Logger.error(f"Error sending email: {e}")
        return {"message": "Error sending registration pass"}, 500

    # redirect to success page
    return redirect(f"{os.getenv('FRONTEND_URL')}/RegistrationSuccess")
