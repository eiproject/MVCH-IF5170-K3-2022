import redis

from core.key import CreatePhysicianKey 


def get_physician_spesialization(db:redis.Redis, hospital_id, physician_id):
    key = CreatePhysicianKey(hospital_id, physician_id)
    specialization = db.hget(key, 'specialization')
    specialization = specialization.decode('utf-8')
    return specialization