def UserKey(hospital_id, user_id):
    return f'{hospital_id}:User[id:{user_id}]'

def UserEmail(user_key:str):
    return user_key.split('id:')[-1].replace(']','')