def CreateUserKey(hospital_id, user_id):
    return f'{hospital_id}:User[id:{user_id}]'

def GetUserIdFromKey(user_key:str):
    return user_key.split('id:')[-1].replace(']','')

def CreatePatientKey(hospital_id, user_id):
    return f'{hospital_id}:Patient[id:{user_id}]'