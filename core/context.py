from datetime import datetime
import redis

from core.key import *


def get_physician_spesialization(db:redis.Redis, region_id, physician_id):
    key = CreatePhysicianKey(region_id, physician_id)
    specialization = db.hget(key, 'specialization')
    specialization = specialization.decode('utf-8')
    return specialization


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
    for phy_id in phy_ids:
        phy_name = phy_id
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
            start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            if start_date.date() == datetime_obj.date():
                day = start_date.strftime('%A')
                time = start_date.strftime('%H:%M')
                date = start_date.strftime('%Y-%m-%d')

                today_phy_sched.append([
                    phy_name, phy_scpecialization, day, date, time, f'{sch_id}:{phy_id}'
                ])

            elif start_date.date() > datetime_obj.date():
                break

    return today_phy_sched