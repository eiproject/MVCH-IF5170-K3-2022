from typing import Tuple
from core.entity import UserType
from core.key import CreatePatientKey, CreatePhysicianScheduleKey, CreateScheduleKey, generate_dummy_schedule
from core.util import check_jwt, get_session_key
from . import app, jwt, db, hospital_id
from flask import Flask, request, render_template, redirect, jsonify, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token
from datetime import datetime, timedelta

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

    # generating timeslot
    now = datetime.now()
    thresh = now + timedelta(days=7)

    key = CreatePhysicianScheduleKey(hospital_id, email)
    schedules_id = [int(v) for v in db.smembers(key)]
    schedules_id.sort()
    
    timeslot = {}
    for id in schedules_id:
        sch_key = CreateScheduleKey(hospital_id, id)
        sch_data = db.hgetall(sch_key)
        start = sch_data[b'start'].decode("utf-8")
        end = sch_data[b'end'].decode("utf-8")

        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        
        date_key = start_date.strftime("%m/%d %A")
        hour = start_date.hour

        if start_date.date() >= now.date() and  start_date.date() < thresh.date():
            if date_key in timeslot:
                timeslot[date_key].append(hour)
            else:
                timeslot[date_key] = [hour]
    
    # rendering 
    header = ['Time']
    for i in range(7):
        t = now + timedelta(days=i)
        d = t.strftime("%m/%d %A")
        header.append(d)

    timeslot_render = [header]

    for hour in range(7, 19):
        row = [f'{hour}:00']
        for d_key in header[1:]:
            if d_key in timeslot:
                if hour in timeslot[d_key]:
                    row.append(True)
                else:
                    row.append(False)
            else:
                row.append(False)
        timeslot_render.append(row)

    return render_template(
        'dashboard/patient-doctor-schedule.html', 
        Name="Doctor Schedule", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=email,
        USER_NAME=email.split('@')[0],
        USER_SPECIALIZATION='Dentist',
        TIMESLOT_HEADER=timeslot_render[0],
        TIMESLOT_ITEM=timeslot_render[1:],
        FROM_TO_SCHEDULE_RANGE=f'from {header[1]} to {header[-1]}',
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
