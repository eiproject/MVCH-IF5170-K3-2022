from . import app, db, region_id
from core.context import get_all_schedule_by_date, get_employee_name, get_upcoming_appointment_schedule, get_user_fullname, get_physician_spesialization
from core.entity import UserType
from core.key import * 
from core.setting import *
from core.util import check_jwt
from datetime import datetime, timedelta
from flask import request, render_template, redirect, session


@app.route("/dashboard", methods=["GET"])
def dashboard():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)
    
    if user_type == UserType.PATIENT:
        template = 'dashboard/patient-home.html'
    elif user_type == UserType.PHYSICIAN:
        template = 'dashboard/doctor-home.html'
    elif user_type == UserType.NURSE:
        template = 'dashboard/nurse-home.html'
    
    # REGISTERED_CONSULTATION_SCHEDULE
    registered_schedule_render = get_upcoming_appointment_schedule(db, region_id, email, user_type)

    # CONSULTATION_SCHEDULE
    phy_sch_today = get_all_schedule_by_date(db, region_id, datetime.now())

    

    return render_template(template, 
        Name="Dashboard", 
        EMAIL=email, 
        USER_TYPE=user_type,
        USER_FULLNAME=user_fullname,
        REGISTERED_CONSULTATION_SCHEDULE=registered_schedule_render,
        CONSULTATION_SCHEDULE=phy_sch_today,
        )


@app.route("/dashboard/patient-registration", methods=["GET"])
def patient_registration():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)

    patient_key = CreatePatientKey(region_id, email)
    if db.hgetall(patient_key):
        return redirect('/dashboard/register-consultation')

    return render_template(
        'dashboard/patient-registration.html', 
        Name="Patient Registration", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=user_fullname,
        )


@app.route("/dashboard/register-consultation", methods=["GET"])
def register_consultation():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)

    timeslots = []
    timeslots_render = []

    physician_id = None
    physician_specialization = None
    physician_name = None

    search_keyword_doctor = request.args.get('doctor')
    search_keyword_date = request.args.get('date')
    
    physicians = db.keys(f'*PhysicianSchedule*{search_keyword_doctor}*')
    physician_sch_key = physicians[0].decode('utf-8') if physicians else None
    
    selected_date = datetime.strptime(search_keyword_date, "%Y-%m-%d") if search_keyword_date else None

    if physician_sch_key:
        physician_id = GetUserIdFromKey(physician_sch_key) 
        physician_specialization = get_physician_spesialization(db, region_id, physician_id)
        physician_name = get_employee_name(db, region_id, physician_id)

        schedule_ids = [int(v) for v in db.smembers(physician_sch_key)] if physician_sch_key else []
        schedule_ids.sort()

        now = datetime.now()
        thresh = now + timedelta(days=7)

        # create timeslots
        for id in schedule_ids:
            sch_key = CreateScheduleKey(region_id, id)
            sch_data = db.hgetall(sch_key)
            start = sch_data[b'start'].decode("utf-8")
            end = sch_data[b'end'].decode("utf-8")

            start_date = datetime.strptime(start, DATE_FORMAT)
            
            is_add = False
            if selected_date is not None:
                if selected_date.date() == start_date.date():
                    is_add = True
            else:
                if start_date.date() >= now.date() and  start_date.date() < thresh.date():
                    is_add = True

            if is_add:
                day = start_date.strftime('%A')
                time = start_date.strftime('%H:%M')
                date = start_date.strftime('%Y-%m-%d')
                timeslots.append([day, time, date, f'{id}:{physician_id}'])

        # rendering 
        for timeslot in timeslots:
            day, time, date, sch_phy = timeslot
            timeslots_render.append([physician_name, physician_specialization, day, date, time, sch_phy])

    elif selected_date:
        timeslots_render = get_all_schedule_by_date(db, region_id, selected_date)
    else:
        timeslots_render = get_all_schedule_by_date(db, region_id, datetime.now())

    return render_template(
        'dashboard/patient-register-consultation.html', 
        Name="Register Consultation", 
        EMAIL=email,
        USER_TYPE=user_type, 
        USER_FULLNAME=user_fullname,
        KEYWORD_DOCTOR=search_keyword_doctor,
        KEYWORD_DATE=search_keyword_date,
        TIMESLOT_ITEM=timeslots_render,
        )

    
@app.route("/dashboard/history-consultation", methods=["GET"])
def history_consultation():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)
    
    if user_type == UserType.PATIENT:
        appointment_key = CreatePatientAppointmentKey(region_id, email)
    elif user_type == UserType.PHYSICIAN:
        appointment_key = CreatePhysicianAppointmentKey(region_id, email)
    elif user_type == UserType.NURSE:
        appointment_key = CreateNurseAppointmentKey(region_id, email)

    appointment_ids = db.smembers(appointment_key)
    appointment_ids = [int(a) for a in appointment_ids]
    appointment_ids.sort()
    
    consultation_history = []

    for app_id in appointment_ids:
        app_key = CreateAppointmentKey(region_id, app_id)
        app_data = db.hgetall(app_key)
        sch_id = int(app_data[b'schedule_id'])
        
        sch_key = CreateScheduleKey(region_id, sch_id)
        sch_data = db.hgetall(sch_key)
        end = sch_data[b'end'].decode('utf-8')
        end_datetime = datetime.strptime(end, DATE_FORMAT)

        if end_datetime < datetime.now():
            physician_id = app_data[b'physician_id'].decode('utf-8')
            physician_specialization = get_physician_spesialization(db, region_id, physician_id)
            physician_name = get_employee_name(db, region_id, physician_id)

            start = sch_data[b'start'].decode('utf-8')
            start_date = datetime.strptime(start, DATE_FORMAT)

            day = start_date.strftime('%A')
            time = start_date.strftime('%H:%M')
            date = start_date.strftime('%Y-%m-%d')
            consultation_history.append([
                physician_name, physician_specialization, day, date, time
            ])

    return render_template(
        'dashboard/history-consultation.html', 
        Name="History Consultation", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=user_fullname,
        COSULTATION_HISTORY=consultation_history,
        )


@app.route("/dashboard/doctor-schedule", methods=["GET"])
def doctor_schedule():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)
    
    # search using input from field
    search_keyword = request.args.get('doctor')
    search_result = db.keys(f'*PhysicianSchedule*{search_keyword}*')
    search_result = search_result[0].decode('utf-8') \
        if search_result else None

    if search_keyword and search_result:
        physician_email = GetUserIdFromKey(search_result)
        physician_key = search_result
        physician_specialization = get_physician_spesialization(db, region_id, physician_email)
        physician_name = get_employee_name(db, region_id, physician_email)
    elif user_type == UserType.PHYSICIAN:
        physician_email = email
        physician_key = CreatePhysicianScheduleKey(region_id, email)
        physician_specialization = get_physician_spesialization(db, region_id, physician_email)
        physician_name = get_employee_name(db, region_id, physician_email)
    else:
        physician_email = ''
        physician_key = ''
        physician_specialization = ''
        physician_name = ''

    # generating timeslot
    now = datetime.now()
    thresh = now + timedelta(days=7)
    schedule_ids = [int(v) for v in db.smembers(physician_key)]
    schedule_ids.sort()
    
    timeslot = {}
    for id in schedule_ids:
        sch_key = CreateScheduleKey(region_id, id)
        sch_data = db.hgetall(sch_key)
        start = sch_data[b'start'].decode("utf-8")
        end = sch_data[b'end'].decode("utf-8")

        start_date = datetime.strptime(start, DATE_FORMAT)
        
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
        USER_FULLNAME=user_fullname,
        PHYSICIAN_NAME=physician_name,
        PHYSICIAN_SPECIALIZATION=physician_specialization,
        TIMESLOT_HEADER=timeslot_render[0],
        TIMESLOT_ITEM=timeslot_render[1:],
        FROM_TO_SCHEDULE_RANGE=f'from {header[1]} to {header[-1]}',
        SEARCH_KEYWORD=search_keyword
        )

@app.route("/dashboard/consultation-schedule", methods=["GET"])
def consultation_schedule():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)
    registered_schedule_render = get_upcoming_appointment_schedule(db, region_id, email, user_type)

    return render_template(
        'dashboard/doctor-consultation-schedule.html', 
        Name="Consultation Schedule", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=user_fullname,
        REGISTERED_CONSULTATION_SCHEDULE=registered_schedule_render,
        )

    
@app.route("/dashboard/patient-list", methods=["GET"])
def patient_list():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)
    
    return render_template(
        'dashboard/doctor-patient-list.html', 
        Name="Patient List", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=user_fullname,
        )

@app.route("/dashboard/nurse-schedule", methods=["GET"])
def nurse_schedule():
    email, user_type = check_jwt(db, session)
    if email is None: return redirect('/logout')
    user_fullname = get_user_fullname(db, region_id, email, user_type)
    
    return render_template(
        'dashboard/nurse-schedule.html', 
        Name="Nurse Schedule", 
        EMAIL=email, 
        USER_TYPE=user_type, 
        USER_FULLNAME=user_fullname,
        )
