from datetime import datetime, timedelta
from typing import Tuple
from core.entity import Region
from core.key import GetUserIdFromKey
from flask import session
from flask_jwt_extended import decode_token


def get_session_key():
    return decode_token(session['jwt'])['sub']


def check_jwt(db, sess) -> Tuple[str, str]:
    user_id_key = None
    if 'jwt' in sess:
        user_id_key = get_session_key()
        data = db.hgetall(user_id_key)
        user_type = data[b'user_type']
        if data:
            return GetUserIdFromKey(user_id_key), user_type.decode("utf-8") 
    
    return None, None

def get_now_datetime(region_id):
    if region_id == Region.INDO:
        return datetime.utcnow() + timedelta(hours=7)
    else:
        return datetime.utcnow() - timedelta(hours=5)
    