import os 
from firebase_admin import auth
from flask import jsonify, make_response
import requests
from api.models.user import User
import dotenv 
dotenv.load_dotenv()

def refresh_token(refresh_token):
    if not refresh_token:
        return jsonify({"error": "No refresh token found in cookies"}), 401

    firebase_api_key = os.getenv('FIREBASE_API_KEY')
    if not firebase_api_key:
        return jsonify({"error": "No API key found"}), 500

    try:
        # Exchange refresh token for new ID token
        response = requests.post(
            f'https://securetoken.googleapis.com/v1/token?key={firebase_api_key}',
            json={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )
        response.raise_for_status()
        data = response.json()

        new_id_token = data['id_token']
        new_refresh_token = data['refresh_token']
        expires_in = data['expires_in']

        # Verify token and get user
        decoded_token = auth.verify_id_token(new_id_token)
        try:
            database_user = User.query.filter_by(fid=decoded_token['user_id']).first()
            user_data = database_user.to_dict() if database_user else None
        except Exception as error:
            print('Error finding user:', error)
            user_data = None

        # Create response with new tokens
        response = make_response(jsonify({
            "message": "Token refreshed successfully",
            "idToken": new_id_token,
            "refreshToken": new_refresh_token,
            "expiresIn": expires_in,
            "user": {**user_data, 'fid': decoded_token['uid']}
        }))

        # Set cookies
        is_production = os.getenv('FLASK_ENV') == 'production'
        response.set_cookie(
            'loginToken',
            new_id_token,
            httponly=True,
            secure=is_production,
            samesite='None' if is_production else 'Lax',
            path='/',
            max_age=7 * 24 * 60 * 60  # 1 week in seconds
        )

        response.set_cookie(
            'refreshToken',
            new_refresh_token,
            httponly=True,
            secure=is_production,
            samesite='None' if is_production else 'Lax',
            path='/',
            max_age=7 * 24 * 60 * 60  # 1 week in seconds
        )

        return response

    except Exception as error:
        print('Error refreshing token:', error)
        return jsonify({
            "message": "Failed to refresh token",
            "error": str(error)
        }), 401