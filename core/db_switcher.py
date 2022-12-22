from typing import List
import redis 
import logging


def get_db_configs():
    with open('db_config', 'r') as file:
        config = file.readlines()
        config = [c.replace('\n', '') for c in config]
        print(config)
        return config


def switch_db_config():
    with open('db_config', 'r') as file:
        config = file.readlines()
        config = [c.replace('\n', '') for c in config]

        with open('db_config', 'w') as file2:
            pop_conf = config.pop(0)
            config.append(pop_conf)
            
            config = [c+'\n' for c in config]
            file2.writelines(config)
            return config


def get_db() -> redis.Redis:
    db = None
    is_ok = True
    db_url = None
    
    while is_ok:
        dbs = get_db_configs()
        # logging.debug(f'Current config: {db_url} {dbs}')
        try:
            db_url = dbs[0]
            db = redis.Redis.from_url(db_url, retry_on_timeout=False, socket_timeout=10)
            ping = db.ping()
            if ping: 
                is_ok = False
            else:
                switch_db_config()
                logging.debug(f'Switching: {db_url} {dbs}')

        except Exception as e:
            # when timeout
            logging.debug(f'Error: {db_url} {dbs} {e}')
            switch_db_config()
        
    return db
