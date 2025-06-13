from flask import request, jsonify, make_response
import firebase_admin
from firebase_admin import auth
import requests
import os
from backend.api.models.user import User
from backend.api import db
from backend.api.utils.logger import Logger

def is_authenticated():
    # extracting token
    auth_token = request.cookies.get('loginToken') or request.json.get('authToken')

    if not auth_token:
        return jsonify({"error": "No authentication token found"}), 401

    try:
        # Verify the token using Firebase Admin
        decoded_token = auth.verify_id_token(auth_token)

        # Find user in database
        user = User.query.filter_by(fid=decoded_token['uid']).first()

        if not user:
            return jsonify({
                "authenticated": False,
                "error": "User not found in database"
            }), 404

        # Token is valid and user exists
        return jsonify({
            "authenticated": True,
            "uid": decoded_token['uid'],
            "user": {**user.to_dict(), 'fid': decoded_token['uid']}
        }), 200

    except Exception as error:
        Logger.error(f"Error verifying token: {str(error)}")
        return jsonify({
            "authenticated": False,
            "error": "Invalid or expired token"
        }), 401

