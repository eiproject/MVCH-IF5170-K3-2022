import time
import redis
from core.setting import DB_SETTING


def write_config_default():
    config = ['redis://35.238.56.161:6379\n', 'redis://34.101.126.53:6379\n']
    with open('db_config', 'w') as file:
        file.writelines(config)


def get_db() -> redis.Redis:
    is_ok = True    
    while is_ok:
        try:
            db_url = DB_SETTING['leader']
            db = redis.Redis.from_url(
                db_url, 
                retry_on_timeout=False, 
                socket_timeout=10
                )
            ping = db.ping()
            if ping: 
                write_config_default()
                time.sleep(60)
            else:
                time.sleep(10)

        except Exception as e:
            print('Error')
            time.sleep(10)
