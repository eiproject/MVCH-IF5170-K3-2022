from hashlib import sha256
from http import HTTPStatus
from flask import jsonify, request, session
from core.context import create_activity

from core.key import CreateUserKey
from . import app, get_db, region_id
from flask_jwt_extended import create_access_token


@app.route("/api/user-register", methods=["POST"])
def register():
    db = get_db()
    code = HTTPStatus.OK
    message = "OK"
    
    email, password = request.form.get('email'), request.form.get('password')
    email = email.lower()

    user_id_key = CreateUserKey(region_id, email)
    is_email_exists = db.hget(user_id_key, 'password')

    if (is_email_exists):
        code = HTTPStatus.BAD_REQUEST
        message = "User already registered."
    else:        
        hashed_pw = sha256(password.encode('utf-8')).hexdigest()
        create_activity(db, region_id, email, 'register')
        db.hset(
            name=user_id_key, 
            mapping={
                'password': hashed_pw,
                'user_type': 'patient',
            }
        )
            
    json_return = {
        "code": code,
        "data": email,
        "message": message
    }
    return jsonify(json_return), code
 

@app.route("/api/user-login", methods=["POST"])
def login():
    db = get_db()
    code = HTTPStatus.OK
    message = "OK"
    jwt_token = None
    
    email, password = request.form.get('email'), request.form.get('password')
    email = email.lower()

    user_id_key = CreateUserKey(region_id, email)

    is_email_exists = db.hget(user_id_key, 'password')

    if (not is_email_exists):
        code = HTTPStatus.BAD_REQUEST
        message = "User not registered."
    else:
        stored_hash = is_email_exists.decode("utf-8") 
        input_hash = sha256(password.encode('utf-8')).hexdigest()
        
        if (stored_hash != input_hash):
            code = HTTPStatus.BAD_REQUEST
            message = "Wrong password."
        else:
            create_activity(db, region_id, email, 'login')
            message = "Login OK"
            jwt_token = create_access_token(identity=user_id_key)
            # store in session
            session['jwt'] = jwt_token

    json_return = {
        "code": code,
        "data": jwt_token,
        "message": message
    }
    return jsonify(json_return), code
