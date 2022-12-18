from typing import Tuple
from core.entity import UserType
from core.key import CreateUserKey, GetUserIdFromKey, CreatePatientKey
from core.util import check_jwt, get_session_key
from . import app, jwt, db, hospital_id
from flask import Flask, request, render_template, redirect, jsonify, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token


@app.route("/dashboard", methods=["GET"])
def dashboard():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')

    if user_type == UserType.PATIENT:
        template = 'dashboard/patient-home.html'
    elif user_type == UserType.DOCTOR:
        template = 'dashboard/doctor-home.html'
    elif user_type == UserType.NURSE:
        template = 'dashboard/nurse-home.html'

    return render_template(template, 
        Name="Dashboard", 
        EMAIL=email, 
        USER_TYPE=user_type,
        USER_FULLNAME=email,
        )


@app.route("/dashboard/patient-registration", methods=["GET"])
def patient_registration():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')

    patient_key = CreatePatientKey(hospital_id, email)
    if db.hgetall(patient_key):
        return redirect('/dashboard/register-consultation')

    return render_template(
        'dashboard/patient-registration.html', 
        Name="Patient Registration", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )


@app.route("/dashboard/register-consultation", methods=["GET"])
def register_consultation():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    return render_template(
        'dashboard/patient-register-consultation.html', 
        Name="Register Consultation", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )

    
@app.route("/dashboard/history-consultation", methods=["GET"])
def history_consultation():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    return render_template(
        'dashboard/history-consultation.html', 
        Name="History Consultation", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )


@app.route("/dashboard/doctor-schedule", methods=["GET"])
def doctor_schedule():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    return render_template(
        'dashboard/patient-doctor-schedule.html', 
        Name="Doctor Schedule", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )

@app.route("/dashboard/consultation-schedule", methods=["GET"])
def consultation_schedule():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    return render_template(
        'dashboard/doctor-consultation-schedule.html', 
        Name="Consultation Schedule", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )

    
@app.route("/dashboard/patient-list", methods=["GET"])
def patient_list():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    return render_template(
        'dashboard/doctor-patient-list.html', 
        Name="Patient List", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )

@app.route("/dashboard/nurse-schedule", methods=["GET"])
def nurse_schedule():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    return render_template(
        'dashboard/nurse-schedule.html', 
        Name="Nurse Schedule", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        )
