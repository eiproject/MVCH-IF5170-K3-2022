from flask_jwt_extended import decode_token
from flask import session

def get_session_mail():
    return decode_token(session['jwt'])['sub']
