"""Mdoules"""
import os
import json
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from api import app
from db import DatabaseConnection
from logging_class import LogManager

from AI_get_data import ElaborationData
from flask_caching import Cache
from flask import current_app

log_manager = LogManager("API_Logs")

load_dotenv()

host = os.getenv("host")
databasename = os.getenv("databasename")
user = os.getenv("user")
password = os.getenv("password")
charset = os.getenv("charset")
port = os.getenv("port")
CLIENT_SECRET=os.getenv("client_secret")
AWS_ACCESS_KEY = os.environ.get('ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('SECRET_KEY')
AWS_END_POINT = os.environ.get('END_POINT')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
WEBHOOK_SECRET=os.getenv('STRIPE_WEBHOOK_SECRET')

MySqlDatabase = DatabaseConnection(host, databasename, charset, user, password, port , log_manager)

app.secret_key = "super-secret"
app.config["JSON_SORT_KEYS"] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)

# CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# Make a regular expression
# for validating an Email
REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# Mail config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

#react routes for reseting password email to redirect to page
REACT_ROUTE="http://34.195.110.86:7034"
# REACT_ROUTE="http://localhost:5173"


#  Following are My Personal credentials
app.config['MAIL_USERNAME'] = 'developercodeaza@gmail.com'
app.config['MAIL_PASSWORD'] = 'zsnsvlvninoizjzs'
mail = Mail(app)

PROJECT_NAME="Home Schooling OZ"
PROJECT_LOGO="https://res.cloudinary.com/de7qyzgg8/image/upload/v1686984824/soberchat-i_obv2gv.png"


# JWT Authentication
app.config["JWT_SECRET_KEY"] = app.secret_key  # This can be changed
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
jwt = JWTManager(app)
blacklist = set()
hashed_otp={}
# file management
app.config["FILES"] = os.path.join(app.root_path, "static/uploads")


# ========================================================================
# This code is for AI model one time execution to get data
# ========================================================================

AI_object = ElaborationData()

def initialize_ai_for_user(user_id):
    log_manager.log("info", "======================")
    log_manager.log("info", "in config function")

    level_ids = AI_object.get_distinct_level_ids(MySqlDatabase, user_id, log_manager)
    user_data = {}

    for level_id in level_ids:
        AI_object.get_elaborations_from_db(MySqlDatabase, level_id, log_manager)
        original_elaborations = AI_object.original_elaborations
        processed_elaborations = AI_object.processed_elaborations

        user_data[str(level_id)] = {
            'original_elaborations': original_elaborations,
            'processed_elaborations': processed_elaborations
        }

    try:
        cached_data = cache.get('users_data') or {}

        cached_data[str(user_id)] = user_data
        cache.set('users_data', cached_data)

    except Exception as e:
        log_manager.log("error", e)
    
    cache_data = cache.get('users_data')
    log_manager.log("success", f"AI model initialized for user: {user_id} \n : {json.dumps(cache_data, indent=4)}")
    log_manager.log("info", "======================")

