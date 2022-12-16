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
    if user_type == UserType.PATIENT:
        return render_template('dashboard/patient-home.html', Name="Dashboard", EMAIL=email)
    elif user_type == UserType.DOCTOR:
        return render_template('dashboard/doctor-home.html', Name="Dashboard", EMAIL=email)


@app.route("/dashboard/patient-registration", methods=["GET"])
def patient_registration():
    email, user_type = check_jwt(session)
    return render_template('dashboard/patient-registration.html', Name="Patient Registration", EMAIL=email)


@app.route("/dashboard/register-consultation", methods=["GET"])
def register_consultation():
    email, user_type = check_jwt(session)
    return render_template('dashboard/patient-register-consultation.html', Name="Register Consultation", EMAIL=email)

    
@app.route("/dashboard/history-consultation", methods=["GET"])
def history_consultation():
    email, user_type = check_jwt(session)
    return render_template('dashboard/patient-history-consultation.html', Name="History Consultation", EMAIL=email)


@app.route("/dashboard/doctor-schedule", methods=["GET"])
def doctor_schedule():
    email, user_type = check_jwt(session)
    return render_template('dashboard/patient-doctor-schedule.html', Name="Doctor Schedule", EMAIL=email)

    