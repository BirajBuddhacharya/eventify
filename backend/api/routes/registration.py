from flask import Blueprint, request
from ..controllers.registration import *
from middleware.auth import verify_club_token, verify_firebase_token, verify_club_admin_token, verify_admin_token
from api.utils.getRelatedBranch import GetRelatedBranch

registration_bp = Blueprint('registration', __name__)

@registration_bp.get("/getTotalRegistration")
def getTotalRegistration(): 
    return GetTotalRegistration()

@registration_bp.post("/registerEvent")
@verify_firebase_token
def registerEvent():
    data = request.get_json()
    user = request.user
    event_id = data.get('event_id')
    return RegisterEvent(user, event_id)

@registration_bp.get("/getAllRegistrations")
def getAllRegistrations(): 
    data = request.get_json()
    user = request.user
    event_id = data.get("event_id")
    
    return GetAllRegistration(user, event_id, data)

@registration_bp.get("/isAlreadyRegistered/<event_id>")
@verify_firebase_token
def isAlreadyRegistered(event_id): 
    user_id = request.user.get('uid')
    return IsAlreadyRegistered(user_id, event_id)

@registration_bp.get("/getEventRegistration/<event_id>")
@verify_club_admin_token
def getEventRegistration(event_id): 
    return GetEventRegistration(event_id)

@registration_bp.get("/getAllRegistrationCount")
@verify_admin_token  
def getAllRegistrationCount(): 
    return GetAllRegistrationCount()

@registration_bp.get("/getBranchRegistrationCount")
@verify_club_token
def getBranchRegistrationCount(): 
    user_id = request.user['uid']
    branch_id =GetRelatedBranch(user_id)
    return GetBranchRegistrationCount(branch_id)

@registration_bp.get("/getRegistrationPass/<event_id>")
@verify_firebase_token
def getRegistrationPass(event_id):
    user_id = request.user['uid']
    return GetRegistrationPass(user_id, event_id)

@registration_bp.get("/verifyRegistration")
def verifyRegistration():
    encrypted_data = request.args.get("encryptedData")
    encrypted_data = encrypted_data.strip("b'").strip("'")
    if not encrypted_data:
        return {"message": "No data provided for verification."}, 400

    return VerifyRegistration(encrypted_data)