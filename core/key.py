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

def CreateNurseScheduleKey(region_id:str, user_id:str) -> str:
    return f'{region_id}:NurseSchedule[id:{user_id}]'

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

def CreateEmployeeKey(region_id:str, user_id:str) -> str:
    # .. region_id:Employee[id:user_id] = name name dob dob address address phone phone gender gender hospital_id hospital_id 
    return f'{region_id}:Employee[id:{user_id}]'

def CreateUserActivityKey(region_id:str, user_id:str) -> str:
    # .. region_id:UserActivity[user_id:user_id] = [ timestamp:page ]
    return f'{region_id}:UserActivity[id:{user_id}]'

# dummy data generator 
def generate_dummy_schedule(db, region_id):
    id = 0
    for day in range(19, 24):
        for hour in range(7, 17):
            key = CreateScheduleKey(region_id, id)
            # format: MM/DD/YYYY HH:MM
            start = f'12/{day}/2022 {hour}:00:00'
            end = f'12/{day}/2022 {hour}:59:59'

            print('start')
            # if not db.hgetall(key):
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

def generate_dummy_nurse_schedule(db, region_id, email):
    import random 
    random.seed(1)
    schedules = random.choices(list(range(0, 50)), k=10)
    key = CreateNurseScheduleKey(region_id, email)
    for s in schedules:
        db.sadd(key, s)


def generate_dummy_employee(db, region_id, email):
    data = {
        'name': 'dr. Ganesha Mulya',
        'dob': '04/08/1980',
        'address': '913-2855 Justo. Rd.',
        'phone': '(026) 7881 4576',
        'gender': 'L',
        'hospital_id': 'mvch001',
    }

    db.hset(
        name=CreateEmployeeKey(region_id, email),
        mapping=data
    )

def generate_dummy_nurse(db, region_id, email):
    # password password_hash user_type user_type
    user_key = CreateUserKey(region_id, email)
    
    # NIC nic specialization specialization
    nurse_key = CreateNurseKey(region_id, email)
    nurse_data = {
        'NIC': '218531458156',
        'specialization': 'Dentist',
    }
    
    # name name dob dob  address address phone phone gender gender hospital_id hospital_id
    employee_key = CreateEmployeeKey(region_id, email)
    employee_data = {
        'name': 'Sernu,ns.',
        'dob': '04/08/1990',
        'address': '913-2855 Justo. Rd.',
        'phone': '(026) 7881 4576',
        'gender': 'L',
        'hospital_id': 'mvch001'
        }

    db.hset(name=employee_key, mapping=employee_data)
    db.hset(name=nurse_key, mapping=nurse_data)




# generate_dummy_schedule(db, region_id)
# generate_dummy_phy_schedule(db, region_id, 'doctor@gmail.com')
# generate_dummy_employee(db, region_id, 'doctor@gmail.com')

# generate_dummy_nurse_schedule(db, region_id, 'nurse@gmail.com')


# hset ID:Physician[id:doctor@gmail.com] NIC 217836271863 specialization Dentist