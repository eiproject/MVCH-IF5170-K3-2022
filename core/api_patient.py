from . import app, db, region_id

from core.entity import UserType
from core.key import *
from core.views_dashboard import check_jwt
from core.context import create_activity, get_patient_information, store_appointment

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

    create_activity(db, region_id, email, 'register patient')
    
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
    print(sch_phy)
    schedule_id, physician_mail = sch_phy.split(':')

    appointment_key = CreatePatientAppointmentKey(region_id, email)
    appointment_ids = db.smembers(appointment_key)

    registered_schedule_ids = []
    for app_id in appointment_ids:
        app_id = int(app_id)
        app_key = CreateAppointmentKey(region_id, app_id)
        sch_id = db.hget(app_key, 'schedule_id')
        registered_schedule_ids.append(int(sch_id))

    if schedule_id not in registered_schedule_ids:
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
    
    create_activity(db, region_id, email, 'create appointment')

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

    json_return = {
        "code": code,
        "data": patient_info,
        "message": message
    }

    create_activity(db, region_id, email, f'see patient information {patient_id}')
    return jsonify(json_return), code
 

