from flask import Blueprint, request, jsonify
from ..models.test import Test
from .. import db
from flask_mail import Message
from api import mail
test_bp = Blueprint('test', __name__)

@test_bp.get('/')
def test(): 
    msg = Message(
        subject='Hello from Flask',
        sender='otakugod0000@gmail.com',
        recipients=['birajbuddhacharya@gmail.com'],
        body='This is a test email from Flask!'
    )
    mail.send(msg)
    return 'Email sent successfully!'