import logging
import os
import redis

from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager

from core.setting import *


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print('BASE_DIR', BASE_DIR)

# Declare Flask app
app = Flask(__name__)

# logger
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
logging.basicConfig(filename='mvch.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Redis
app.config['SECRET_KEY'] = 'BDy9asydnasdna98n^B&D*tsa87dvbats67asrv67r'

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "s0m37h1ng53cr37**&SA*&%^&*%*^*("
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1440)
app.config["JWT_ERROR_MESSAGE_KEY"] = "Error"

# Public class
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

region_id = DB_SETTING['region_id']
redis_dbs = [DB_SETTING['leader'], DB_SETTING['follower']]

def get_db() -> redis.Redis:
    db = None
    is_ok = True
    db_url = None
    
    # counter = 0
    while is_ok:
        try:
            db_url = redis_dbs[0]
            db = redis.Redis.from_url(db_url, retry_on_timeout=False, socket_timeout=10)
            ping = db.ping()
            if ping: 
                is_ok = False
            else:
                lead, foll = redis_dbs[0], redis_dbs[0]
                redis_dbs = [foll, lead]

        except Exception as e:
            # when timeout
            logging.debug(f'Error: {db_url} {e} |  {type(e)}')
            lead, foll = redis_dbs[0], redis_dbs[0]
            redis_dbs = [foll, lead]
        
        # counter+=1
    return db

logging.debug(f'Starting app..')

from core import \
    views, views_dashboard, \
    api_user, api_patient, \
    error_handler, jwt_test