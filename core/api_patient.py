from . import app, db, region_id

from core.entity import UserType
from core.key import CreatePatientKey, GetUserIdFromKey
from core.views_dashboard import check_jwt
from core.context import get_patient_information, store_appointment

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

    patient_key = CreatePatientKey(region_id, email)
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

    json_return = {
        "code": code,
        "data": 'OK',
        "message": message
    }
    return jsonify(json_return), code
 

@app.route("/api/create-appointment", methods=["POST"])
def create_appointment():
    code = HTTPStatus.OK
    message = "OK"
    email, user_type = check_jwt(db, session)
    if user_type != UserType.PATIENT:
        return jsonify({"message": "Only for patient"}), 400

    patient_key = CreatePatientKey(region_id, email)
    if not db.hgetall(patient_key):
        return jsonify({"message": "Only for Registered patient"}), 400

    sch_phy = request.form.get('sch_phy')
    schedule_id, physician_mail = sch_phy.split(':')

    store_appointment(
        db=db, 
        region_id=region_id, 
        schedule_id=schedule_id, 
        patient_id=email, 
        physician_id=physician_mail,
        nurse_id='-',
        notes='-',
        )

    json_return = {
        "code": code,
        "data": 'OK',
        "message": message
    }
    return jsonify(json_return), code
 

@app.route("/api/patient-information", methods=["POST"])
def patient_information():
    code = HTTPStatus.OK
    message = "OK"
    email, user_type = check_jwt(db, session)
    if user_type != UserType.PHYSICIAN:
        return jsonify({"message": "Only for physician"}), 400

    patient_id = request.form.get('user_id')
    patient_info = get_patient_information(db, region_id, patient_id)
    print(patient_info)
    json_return = {
        "code": code,
        "data": patient_info,
        "message": message
    }
    return jsonify(json_return), code
 

