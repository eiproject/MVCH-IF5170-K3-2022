import time
import redis


def write_config_default():
    config = ['redis://34.101.126.53:6379\n', 'redis://35.238.56.161:6379\n']
    with open('db_config', 'w') as file:
        file.writelines(config)


def auto_switching_db() -> redis.Redis:
    is_ok = True    
    while is_ok:
        try:
            db_url = 'redis://34.101.126.53:6379'
            db = redis.Redis.from_url(
                db_url, 
                retry_on_timeout=False, 
                socket_timeout=10
                )
            ping = db.ping()
            if ping: 
                print('ok')
                write_config_default()
                time.sleep(60)
            else:
                print('not ok')
                time.sleep(10)

        except Exception as e:
            print(f'Error, {e}')
            time.sleep(10)

if __name__ == '__main__':
    auto_switching_db()