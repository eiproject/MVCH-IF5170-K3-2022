import logging
import os
import redis

from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager

from core.setting import *
from core.db_switcher import get_db

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
dbs = [DB_SETTING['leader'], DB_SETTING['follower']]

logging.debug(f'Starting app..')

from core import \
    views, views_dashboard, \
    api_user, api_patient, \
    error_handler, jwt_test