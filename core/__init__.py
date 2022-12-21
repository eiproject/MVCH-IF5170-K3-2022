import logging
import os
import redis

from datetime import timedelta
from flask import Flask
from flask_redis import FlaskRedis
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
app.config['SECRET_KEY'] = 'changethis_BDy9asydnasdna98n^B&D*tsa87dvbats67asrv67r'
if 'rizquuula/Playground/' in BASE_DIR:
    app.config['REDIS_URL'] = 'redis://34.101.126.53:6379'
else:
    app.config['REDIS_URL'] = 'redis://34.101.111.202:6379'

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "changethis_s0m37h1ng53cr37**&SA*&%^&*%*^*("
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1440)
app.config["JWT_ERROR_MESSAGE_KEY"] = "Error"

# Public class
jwt = JWTManager(app)

db:redis.Redis = FlaskRedis(app)
db.init_app(app)

bcrypt = Bcrypt(app)

region = 'indo'
region_id = 'indo'

from core import \
    views, views_dashboard, \
    api_user, api_patient, \
    error_handler, jwt_test
