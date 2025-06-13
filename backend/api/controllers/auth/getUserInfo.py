from flask import request, jsonify, make_response
from firebase_admin import auth
from backend.api.utils.logger import Logger
from backend.api import db
from backend.api.models.user import User

def GetUserInfo():
    # Check if content type is application/json when request has body
    if request.method == 'POST' and not request.is_json:
        return jsonify({
            "error": "Content-Type must be application/json"
        }), 415

    # Get auth token from cookies or request body
    auth_token = request.cookies.get('loginToken')
    if request.is_json:
        auth_token = auth_token or request.json.get('authToken')

    if not auth_token:
        return jsonify({"error": "No authentication token found"}), 401

    try:
        # Verify the token using Firebase Admin
        decoded_token = auth.verify_id_token(auth_token)

    except Exception as error:
        Logger.error(f"Error verifying token: {str(error)}")
        return jsonify({
            "authenticated": False,
            "error": "Invalid or expired token"
        }), 401
        
    try:
        user = User.query.filter_by(fid=decoded_token['uid']).first()
    except Exception as error:
        Logger.error(f"Error finding user: {str(error)}")
        user = None
        # Create new user if doesn't exist
        if not user:
            return jsonify({
                "authenticated": False,
                "error": "User not found in database"
            }), 401
    
    # formating data
    return jsonify({
        "fid": decoded_token['uid'],
        "email": decoded_token.get("email", None),
        "imageUrl": user.imageUrl, 
        "role": user.role
    })
