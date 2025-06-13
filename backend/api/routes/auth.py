from flask import Blueprint, request, jsonify
from backend.api import db 
from api.controllers.auth import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.get("/test")
def test(): 
    return 'test'

@auth_bp.post("/signin")
def signin():
    return signin_controller()

@auth_bp.post("/register")
def register(): 
    return register_controller(request)

@auth_bp.post("/signin-with-google")
def signin_with_google(): 
    return SigninWithGoogleController(request)

@auth_bp.get("/is-authenticated")
def check_auth():
    return is_authenticated()

@auth_bp.post("/logout")
def logout_user():
    return logout()

@auth_bp.post("/refresh")
def refresh():
    token = request.cookies.get('refreshToken')
    return refresh_token(token)

@auth_bp.get("/getUserInfo")
def getUserInfo(): 
    return GetUserInfo()
    
    