from hashlib import sha256
from http import HTTPStatus
from flask import jsonify, request, session

from core.key import CreateUserKey
from . import app, db, BASE_DIR, region, region_id
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


@app.route("/api/user-register", methods=["POST"])
def register():
    code = HTTPStatus.OK
    message = "OK"
    email, password = request.form.get('email'), request.form.get('password')
    user_id_key = CreateUserKey(region_id, email)
    is_email_exists = db.hget(user_id_key, 'password')

    if (is_email_exists):
        code = HTTPStatus.BAD_REQUEST
        message = "User already registered."
    else:        
        hashed_pw = sha256(password.encode('utf-8')).hexdigest()
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
    code = HTTPStatus.OK
    message = "OK"
    jwt_token = None
    email, password = request.form.get('email'), request.form.get('password')
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
