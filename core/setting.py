DATE_FORMAT = "%m/%d/%Y %H:%M:%S"

DB_SETTING = {
    'region_id': 'indo',
    'leader': 'redis://34.101.126.53:6379',
    'follower': 'redis://35.238.56.161:6379',
}

REDIS_DBS = [DB_SETTING['leader'], DB_SETTING['follower']]