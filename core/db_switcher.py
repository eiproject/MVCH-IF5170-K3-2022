from typing import List
import redis 
import logging


def get_db(dbs: List[str]) -> redis.Redis:
    db = None
    is_ok = True
    db_url = None
    
    # counter = 0
    while is_ok:
        try:
            db_url = dbs[0]
            db = redis.Redis.from_url(db_url, retry_on_timeout=False, socket_timeout=10)
            ping = db.ping()
            if ping: 
                is_ok = False
            else:
                lead, foll = dbs[0], dbs[1]
                dbs = [foll, lead]

        except Exception as e:
            # when timeout
            logging.debug(f'Error: {db_url} {dbs} {e}')
            lead, foll = dbs[0], dbs[1]
            dbs = [foll, lead]
        
        # counter+=1
    return db