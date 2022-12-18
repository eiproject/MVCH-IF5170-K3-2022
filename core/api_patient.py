from . import app, db, hospital_id

from core.entity import UserType
from core.key import CreatePatientKey, GetUserIdFromKey
from core.views_dashboard import check_jwt

from flask import jsonify, request, session
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus


@app.route("/api/patient-register", methods=["POST"])
def register_patient():
    code = HTTPStatus.OK
    message = "OK"
    email, user_type = check_jwt(db, session)
    if user_type != UserType.PATIENT:
        return jsonify({"message": "Only for patient"}), 400

    patient_key = CreatePatientKey(hospital_id, email)
    if db.hgetall(patient_key):
        return jsonify({"message": "Only for unregistered patient"}), 400

    fullname, gender, dob, address, phone = \
        request.form.get('pfn'), \
        request.form.get('pg'), \
        request.form.get('pdob'), \
        request.form.get('padd'), \
        request.form.get('ppn')

    db.hset(
        name=patient_key, 
        mapping={
            'name': fullname,
            'dob': dob,
            'address': address,
            'phone': phone,
            'gender': gender,
        }
    )
    print(patient_key)
    json_return = {
        "code": code,
        "data": 'OK',
        "message": message
    }
    return jsonify(json_return), code
 

# @app.route("/api/user-login", methods=["POST"])
# def login():
#     code = HTTPStatus.OK
#     message = "OK"
#     jwt_token = None
#     email, password = request.form.get('email'), request.form.get('password')
#     user_id_key = CreateUserKey(hospital_id, email)

#     is_email_exists = db.hget(user_id_key, 'password')
#     print(user_id_key)
#     if (not is_email_exists):
#         code = HTTPStatus.BAD_REQUEST
#         message = "User not registered."
#     else:
#         stored_hash = is_email_exists.decode("utf-8") 
#         input_hash = sha256(password.encode('utf-8')).hexdigest()
        
#         if (stored_hash != input_hash):
#             code = HTTPStatus.BAD_REQUEST
#             message = "Wrong password."
#         else:
#             message = "Login OK"
#             jwt_token = create_access_token(identity=user_id_key)
#             # store in session
#             session['jwt'] = jwt_token

#     json_return = {
#         "code": code,
#         "data": jwt_token,
#         "message": message
#     }
#     return jsonify(json_return), code
