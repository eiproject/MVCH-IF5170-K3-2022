def CreateUserKey(hospital_id:str, user_id:str) -> str:
    return f'{hospital_id}:User[id:{user_id}]'

def GetUserIdFromKey(user_key:str) -> str:
    return user_key.split('id:')[-1].replace(']','')

def CreatePatientKey(hospital_id:str, user_id:str) -> str:
    return f'{hospital_id}:Patient[id:{user_id}]'

def CreatePhysicianKey(hospital_id:str, user_id:str) -> str:
    return f'{hospital_id}:Physician[id:{user_id}]'

def CreateNurseKey(hospital_id:str, user_id:str) -> str:
    return f'{hospital_id}:Nurse[id:{user_id}]'

def CreateScheduleKey(hospital_id:str, schedule_id:int) -> str:
    return f'{hospital_id}:Schedule[id:{schedule_id}]'

def CreatePhysicianScheduleKey(hospital_id:str, user_id:str) -> str:
    return f'{hospital_id}:PhysicianSchedule[id:{user_id}]'

def CreateAppointmentKey(hospital_id:str, appointment_id:int) -> str:
    return f'{hospital_id}:Appointment[id:{appointment_id}]'

def CreateLatestAppointmentIdKey(hospital_id:str) -> str:
    return f'{hospital_id}:Appointment:latest_id'

def CreatePatientAppointmentKey(hospital_id:str, user_id:str) -> str:
    return f'{CreatePatientKey(hospital_id, user_id)}:Appointment'

def CreatePhysicianAppointmentKey(hospital_id:str, user_id:str) -> str:
    return f'{CreatePhysicianKey(hospital_id, user_id)}:Appointment'

def CreateNurseAppointmentKey(hospital_id:str, user_id:str) -> str:
    return f'{CreateNurseKey(hospital_id, user_id)}:Appointment'

# dummy data generator 
def generate_dummy_schedule(db, hospital_id):
    id = 0
    for day in range(19, 24):
        for hour in range(7, 17):
            key = CreateScheduleKey(hospital_id, id)
            start = f'2022-12-{day}T{hour}:00:00'
            end = f'2022-12-{day}T{hour}:59:59'
            if not db.hgetall(key):
                db.hset(
                    name=key, 
                    mapping={
                        'start': start,
                        'end': end,
                    }
                )
            id+=1

def generate_dummy_phy_schedule(db, hospital_id, email):
    import random 
    random.seed(1)
    schedules = random.choices(list(range(0, 50)), k=10)
    key = CreatePhysicianScheduleKey(hospital_id, email)
    for s in schedules:
        db.sadd(key, s)


# generate_dummy_schedule(db, hospital_id)
# generate_dummy_phy_schedule(db, hospital_id, 'doctor@gmail.com')


# hset ID:Physician[id:doctor@gmail.com] NIC 217836271863 specialization Dentist