def CreateUserKey(region_id:str, user_id:str) -> str:
    return f'{region_id}:User[id:{user_id}]'

def GetUserIdFromKey(user_key:str) -> str:
    return user_key.split('id:')[-1].replace(']','')

def CreatePatientKey(region_id:str, user_id:str) -> str:
    return f'{region_id}:Patient[id:{user_id}]'

def CreatePhysicianKey(region_id:str, user_id:str) -> str:
    return f'{region_id}:Physician[id:{user_id}]'

def CreateNurseKey(region_id:str, user_id:str) -> str:
    return f'{region_id}:Nurse[id:{user_id}]'

def CreateScheduleKey(region_id:str, schedule_id:int) -> str:
    return f'{region_id}:Schedule[id:{schedule_id}]'

def CreatePhysicianScheduleKey(region_id:str, user_id:str) -> str:
    return f'{region_id}:PhysicianSchedule[id:{user_id}]'

def CreateAppointmentKey(region_id:str, appointment_id:int) -> str:
    return f'{region_id}:Appointment[id:{appointment_id}]'

def CreateLatestAppointmentIdKey(region_id:str) -> str:
    return f'{region_id}:Appointment:latest_id'

def CreatePatientAppointmentKey(region_id:str, user_id:str) -> str:
    return f'{CreatePatientKey(region_id, user_id)}:Appointment'

def CreatePhysicianAppointmentKey(region_id:str, user_id:str) -> str:
    return f'{CreatePhysicianKey(region_id, user_id)}:Appointment'

def CreateNurseAppointmentKey(region_id:str, user_id:str) -> str:
    return f'{CreateNurseKey(region_id, user_id)}:Appointment'

# dummy data generator 
def generate_dummy_schedule(db, region_id):
    id = 0
    for day in range(19, 24):
        for hour in range(7, 17):
            key = CreateScheduleKey(region_id, id)
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

def generate_dummy_phy_schedule(db, region_id, email):
    import random 
    random.seed(1)
    schedules = random.choices(list(range(0, 50)), k=10)
    key = CreatePhysicianScheduleKey(region_id, email)
    for s in schedules:
        db.sadd(key, s)


# generate_dummy_schedule(db, region_id)
# generate_dummy_phy_schedule(db, region_id, 'doctor@gmail.com')


# hset ID:Physician[id:doctor@gmail.com] NIC 217836271863 specialization Dentist