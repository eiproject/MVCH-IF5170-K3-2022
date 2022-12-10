from hashlib import sha256
from http import HTTPStatus
from flask import jsonify, request, session
from . import app, db, BASE_DIR
from .models import Users

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@app.route("/api/user-register", methods=["POST"])
def register():
    code = HTTPStatus.OK
    message = "OK"
    email, password, retypepassword = request.form.get('email'), \
                                    request.form.get('password'), \
                                    request.form.get('retypepassword')
    if (Users.query.filter_by(email=email).first()):
        code = HTTPStatus.BAD_REQUEST
        message = "User already registered."
    else:        
        if (password != retypepassword):
            code = HTTPStatus.BAD_REQUEST
            message = "Password not match."
        else:
            hashed_pw = sha256(password.encode('utf-8')).hexdigest()
            query_new_user = Users(
                        email=email,
                        password_hash= hashed_pw
                    )
            db.session.add(query_new_user)
            db.session.commit()

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
    email, password = request.form.get('email'), \
                                    request.form.get('password')

    check_user = Users.query.filter_by(email=email).first()
    if (not check_user):
        code = HTTPStatus.BAD_REQUEST
        message = "Login failed (1)."
    else:   
        hash = sha256(password.encode('utf-8')).hexdigest()     
        if (hash != check_user.password_hash):
            code = HTTPStatus.BAD_REQUEST
            message = "Login failed (2)."
        else:
            message = "Login OK"

            jwt_token = create_access_token(identity=email)
            # store in session
            session['jwt'] = jwt_token

    json_return = {
        "code": code,
        "data": jwt_token,
        "message": message
    }
    return jsonify(json_return), code
