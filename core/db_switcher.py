import redis 
import logging
from core.setting import REDIS_DBS


def get_db() -> redis.Redis:
    db = None
    is_ok = True
    db_url = None
    
    # counter = 0
    while is_ok:
        try:
            db_url = REDIS_DBS[0]
            db = redis.Redis.from_url(db_url, retry_on_timeout=False, socket_timeout=10)
            ping = db.ping()
            if ping: 
                is_ok = False
            else:
                lead, foll = REDIS_DBS[0], REDIS_DBS[1]
                REDIS_DBS = [foll, lead]

        except Exception as e:
            # when timeout
            logging.debug(f'Error: {db_url} {e} |  {type(e)}')
            lead, foll = REDIS_DBS[0], REDIS_DBS[1]
            REDIS_DBS = [foll, lead]
        
        # counter+=1
    return db