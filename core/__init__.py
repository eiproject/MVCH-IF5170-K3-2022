import logging
import os
import redis

from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager


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
# if 'rizquuula/Playground/' in BASE_DIR:
#     app.config['REDIS_URL'] = 'redis://34.101.111.202:6379'
# else:
#     app.config['REDIS_URL'] = 'redis://34.101.111.202:6379'

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "s0m37h1ng53cr37**&SA*&%^&*%*^*("
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1440)
app.config["JWT_ERROR_MESSAGE_KEY"] = "Error"

# Public class
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

region = 'indo'
region_id = 'indo'


def get_db() -> redis.Redis:
    db = None
    leader = 'redis://34.101.111.202:6379'
    follower = 'redis://34.135.238.181:6379'
    
    redis_dbs = [leader, follower]
    
    is_ok = True
    counter = 0
    while is_ok:
        try:
            db_url = redis_dbs[counter%2]
            logging.debug(f'Trying to connect {db_url}')
            
            db = redis.Redis.from_url(db_url, retry_on_timeout=False, socket_timeout=10)
            ping = db.ping()
            
            if ping:
                logging.debug(f'Connected {db_url}')
                is_ok = False
        except Exception as e:
            # when timeout
            logging.debug(f'Error: {e} |  {type(e)}')
        
        counter+=1
    return db

logging.debug(f'Starting app..')

from core import \
    views, views_dashboard, \
    api_user, api_patient, \
    error_handler, jwt_test