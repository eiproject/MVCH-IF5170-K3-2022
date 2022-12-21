from datetime import datetime, timedelta
import logging
import redis
from core.entity import UserType

from core.key import *
from core.setting import *
from core.util import get_now_datetime


def get_physician_spesialization(db:redis.Redis, region_id, physician_id):
    key = CreatePhysicianKey(region_id, physician_id)
    specialization = db.hget(key, 'specialization')
    specialization = specialization.decode('utf-8') if specialization else ''
    return specialization

def get_nurse_spesialization(db:redis.Redis, region_id, nurse_id):
    key = CreateNurseKey(region_id, nurse_id)
    specialization = db.hget(key, 'specialization')
    specialization = specialization.decode('utf-8') if specialization else ''
    return specialization

def get_employee_name(db:redis.Redis, region_id, user_id):
    key = CreateEmployeeKey(region_id, user_id)
    name = db.hget(key, 'name')
    name = name.decode('utf-8') if name else user_id.split('@')[0]
    return name

def get_user_fullname(db:redis.Redis, region_id, user_id, user_type):
    if user_type == UserType.PATIENT:
        key = CreatePatientKey(region_id, user_id)
    else:
        key = CreateEmployeeKey(region_id, user_id)

    name = db.hget(key, 'name')
    if name:
        name = name.decode('utf-8')
    else:
        name = user_id.split('@')[0]
    return name

def store_appointment(db:redis.Redis, region_id, schedule_id, patient_id, physician_id, nurse_id, notes):
    latest_app_key = CreateLatestAppointmentIdKey(region_id)
    
    # check latest appointment id
    latest_app_id = db.get(latest_app_key)
    if latest_app_id is None:
        db.set(latest_app_key, -1)
        latest_app_id = -1
    else:
        latest_app_id = int(latest_app_id)

    appointment_id = latest_app_id+1

    appointment_key = CreateAppointmentKey(region_id, appointment_id)
    patient_appointment_key = CreatePatientAppointmentKey(region_id, patient_id)
    physician_appointment_key = CreatePhysicianAppointmentKey(region_id, physician_id)
    nurse_appointment_key = CreateNurseAppointmentKey(region_id, nurse_id)

    db.hset(
        name=appointment_key, 
        mapping={
            'schedule_id': schedule_id,
            'patient_id': patient_id,
            'physician_id': physician_id,
            'nurse_id': nurse_id,
            'notes': notes,
        }
    )

    db.sadd(patient_appointment_key, appointment_id)
    db.sadd(physician_appointment_key, appointment_id)
    db.sadd(nurse_appointment_key, appointment_id)

    db.set(latest_app_key, appointment_id)
    return 

def get_all_physician_id(db:redis.Redis, region_id):
    physicians = db.keys(f'*{region_id}*PhysicianSchedule*')
    physician_ids = []
    for phy_sch_id in physicians:
        physician_ids.append(
            GetUserIdFromKey(phy_sch_id.decode('utf-8'))
        )
    return physician_ids
    

def get_all_schedule_by_date(db:redis.Redis, region_id, datetime_obj:datetime):
    today_phy_sched = []

    phy_ids = get_all_physician_id(db, region_id)

    max = 10
    counter = 0
    for phy_id in phy_ids:
        print(counter)
        phy_name = get_employee_name(db, region_id, phy_id)
        phy_scpecialization = get_physician_spesialization(db, region_id, phy_id)

        # loop to phy schedule and get today schedule
        phy_sch_key = CreatePhysicianScheduleKey(region_id, phy_id)
        
        sch_list = db.smembers(name=phy_sch_key)
        sch_list = [int(v) for v in sch_list]
        sch_list.sort()

        for sch_id in sch_list:
            sch_key = CreateScheduleKey(region_id, sch_id)

            sch_data = db.hgetall(sch_key)
            start = sch_data[b'start'].decode('utf-8')
            start_date = datetime.strptime(start, DATE_FORMAT)
            if start_date.date() == datetime_obj.date():
                day = start_date.strftime('%A')
                time = start_date.strftime('%H:%M')
                date = start_date.strftime('%Y-%m-%d')
                
                is_available = start_date > datetime_obj

                today_phy_sched.append([
                    phy_name, phy_scpecialization, day, date, time, f'{sch_id}:{phy_id}', is_available
                ])

            elif start_date.date() > datetime_obj.date():
                break

        # if counter >= max:
        #     break 

        counter+=1

    return today_phy_sched


def get_upcoming_appointment_schedule(db:redis.Redis, region_id, user_id, user_type):
    now = get_now_datetime(region_id)
    appointment_key = None

    if user_type == UserType.PATIENT:
        appointment_key = CreatePatientAppointmentKey(region_id, user_id)
    elif user_type == UserType.PHYSICIAN:
        appointment_key = CreatePhysicianAppointmentKey(region_id, user_id)
    elif user_type == UserType.NURSE:
        appointment_key = CreateNurseAppointmentKey(region_id, user_id)

    upcoming_appointments = []
    appointment_ids = db.smembers(appointment_key)
    appointment_ids = [int(v) for v in appointment_ids] if appointment_ids else []

    for id in appointment_ids:
        app_key = CreateAppointmentKey(region_id, id)
        app_data = db.hgetall(app_key)
        
        if not app_data: raise Exception('Appointment is not exists')

        schedule_id = app_data[b'schedule_id'].decode('utf-8')
        sch_key = CreateScheduleKey(region_id, schedule_id)
        sch_data = db.hgetall(sch_key)
        start = sch_data[b'start'].decode('utf-8')

        start_date = datetime.strptime(start, DATE_FORMAT)

        if start_date > now:
            physician_id = app_data[b'physician_id'].decode('utf-8')
            physician_specialization = get_physician_spesialization(db, region_id, physician_id)
            physician_name = get_employee_name(db, region_id, physician_id)

            patient_id = app_data[b'patient_id'].decode('utf-8')
            patient_name = get_user_fullname(db, region_id, patient_id, UserType.PATIENT)

            day = start_date.strftime('%A')
            time = start_date.strftime('%H:%M')
            date = start_date.strftime('%Y-%m-%d')
            upcoming_appointments.append([
                physician_name, physician_specialization, day, date, time, patient_name, patient_id
            ])

    upcoming_appointments.sort(key=lambda x: (x[3], x[4]))
    return upcoming_appointments

def calculate_age(born: datetime):
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def get_patient_information(db:redis.Redis, region_id, user_id):
    patient_key = CreatePatientKey(region_id, user_id)
    patient_data = db.hgetall(patient_key)

    patient_name = patient_data[b'name'].decode('utf-8')
    patient_dob = patient_data[b'dob'].decode('utf-8')
    patient_address = patient_data[b'address'].decode('utf-8')
    patient_phone = patient_data[b'phone'].decode('utf-8')
    patient_gender = patient_data[b'gender'].decode('utf-8')
    
    patient_dob_datetime = datetime.strptime(patient_dob, "%m/%d/%Y")

    if patient_gender.lower() == 'm':
        patient_gender = 'Male'
    else:
        patient_gender = 'Female'

    info = {
        'name': patient_name,
        'age': calculate_age(patient_dob_datetime),
        'address': patient_address,
        'phone': patient_phone,
        'gender': patient_gender,
    }

    return info


def get_nurse_schedule(db:redis.Redis, region_id, nurse_id, is_future=True):
    now = get_now_datetime(region_id)
    nurse_sch_key = CreateNurseScheduleKey(region_id, nurse_id)
    nurse_sch_ids = db.smembers(nurse_sch_key)
    nurse_sch_ids = sorted([int(i) for i in nurse_sch_ids])

    nurse_specialization = get_nurse_spesialization(db, region_id, nurse_id)

    phy_sch_data = {}

    phy_sch_keys = db.keys('*PhysicianSchedule*')
    for phy_sch_key in phy_sch_keys:
        phy_id = GetUserIdFromKey(phy_sch_key.decode('utf-8'))
        phy_specialization = get_physician_spesialization(db, region_id, phy_id)
        
        if nurse_specialization == phy_specialization:
            phy_sch_ids = db.smembers(phy_sch_key)
            phy_sch_ids = sorted([int(i) for i in phy_sch_ids])
            phy_sch_data[phy_id] = phy_sch_ids

    logging.debug(msg=str(phy_sch_data))
    logging.debug(msg=str(nurse_sch_ids))
    
    nurse_sch_data = {}

    for nurse_sch_id in nurse_sch_ids:
        sch_key = CreateScheduleKey(region_id, nurse_sch_id)
        start = db.hget(sch_key, 'start').decode('utf-8')
        start_date = datetime.strptime(start, DATE_FORMAT)

        if is_future:
            is_valid = start_date.date() >= now.date()
        else:
            is_valid = start_date.date() < now.date()

        if is_valid:
            day = start_date.strftime('%A')
            time = start_date.strftime('%H:%M')
            date = start_date.strftime('%Y-%m-%d')

            physician = []
            for k in phy_sch_data:
                if nurse_sch_id in  phy_sch_data[k]:
                    physician_name = get_employee_name(db, region_id, k)
                    physician.append(physician_name)
            
            nurse_sch_data[nurse_sch_id] = {
                'day': day,
                'time': time,
                'date': date,
                'speciality': nurse_specialization,
                'physician': physician,
            }

    print(nurse_sch_data)
    return nurse_sch_data


def create_activity(db:redis.Redis, region_id, user_id, activity):
    key = CreateUserActivityKey(region_id, user_id)
    timestamp = get_now_datetime(region_id).isoformat()
    value = f'{timestamp}:{activity}'
    db.sadd(key, value)
