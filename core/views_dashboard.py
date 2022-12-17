from typing import Tuple
from core.entity import UserType
from core.util import get_session_mail
from . import app, jwt, db
from flask import Flask, request, render_template, redirect, jsonify, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token


def check_jwt(sess) -> Tuple[str, str]:
    email = None
    if 'jwt' in sess:
        email = get_session_mail()
        data = db.hgetall(email)
        user_type = data[b'user_type']
        if data:
            return email, user_type.decode("utf-8") 
        else:
            return redirect('/logout')
            

@app.route("/dashboard", methods=["GET"])
def dashboard():
    email, user_type = check_jwt(session)
    user_type = UserType.NURSE # override for dev
    if user_type == UserType.PATIENT:
        return render_template('dashboard/patient-home.html', Name="Dashboard", EMAIL=email, USER_TYPE=user_type)
    elif user_type == UserType.DOCTOR:
        return render_template('dashboard/doctor-home.html', Name="Dashboard", EMAIL=email, USER_TYPE=user_type)
    elif user_type == UserType.NURSE:
        return render_template('dashboard/nurse-home.html', Name="Dashboard", EMAIL=email, USER_TYPE=user_type)


@app.route("/dashboard/patient-registration", methods=["GET"])
def patient_registration():
    email, user_type = check_jwt(session)
    return render_template('dashboard/patient-registration.html', Name="Patient Registration", EMAIL=email, USER_TYPE=user_type)


@app.route("/dashboard/register-consultation", methods=["GET"])
def register_consultation():
    email, user_type = check_jwt(session)
    return render_template('dashboard/patient-register-consultation.html', Name="Register Consultation", EMAIL=email, USER_TYPE=user_type)

    
@app.route("/dashboard/history-consultation", methods=["GET"])
def history_consultation():
    email, user_type = check_jwt(session)
    user_type = UserType.NURSE # override for dev
    return render_template('dashboard/history-consultation.html', Name="History Consultation", EMAIL=email, USER_TYPE=user_type)


@app.route("/dashboard/doctor-schedule", methods=["GET"])
def doctor_schedule():
    email, user_type = check_jwt(session)
    user_type = UserType.DOCTOR # override for dev
    return render_template('dashboard/patient-doctor-schedule.html', Name="Doctor Schedule", EMAIL=email, USER_TYPE=user_type)

@app.route("/dashboard/consultation-schedule", methods=["GET"])
def consultation_schedule():
    email, user_type = check_jwt(session)
    user_type = UserType.DOCTOR # override for dev
    return render_template('dashboard/doctor-consultation-schedule.html', Name="Consultation Schedule", EMAIL=email, USER_TYPE=user_type)

    
@app.route("/dashboard/patient-list", methods=["GET"])
def patient_list():
    email, user_type = check_jwt(session)
    user_type = UserType.DOCTOR # override for dev
    return render_template('dashboard/doctor-patient-list.html', Name="Patient List", EMAIL=email, USER_TYPE=user_type)

@app.route("/dashboard/nurse-schedule", methods=["GET"])
def nurse_schedule():
    email, user_type = check_jwt(session)
    user_type = UserType.NURSE # override for dev
    return render_template('dashboard/nurse-schedule.html', Name="Nurse Schedule", EMAIL=email, USER_TYPE=user_type)
