"""Modules"""
# imports
import os
from flask_restful import Api
import sentry_sdk

from dotenv import load_dotenv
load_dotenv()
sentry_dsn = os.getenv("dsn")
sentry_enabled = os.getenv("sentry_enabled")

# API ROUTES IMPORT
from app import app
from user import User
from webhooks import Webhook
from user_account import UserAccount
from plan import Plan
from child import Children
from report import Reports
from subject_data import Levels
from subject_data import SubjectData
from subscriber import Subscriber
from activity import Activity
from download_activity import DownloadActivity
from state_terms import States
from subject import Subjects
from AI_activity import AIActivity

# Api Creation
api = Api(app)

if sentry_enabled =="True":
    sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0
        )


# ROUTES


@app.route("/")
def home():
    """Home Page Route"""
    return "Home-Schooling APIs"


api.add_resource(User, "/User")
api.add_resource(UserAccount, "/UserAccount")
api.add_resource(Plan, "/Plans")
api.add_resource(Subscriber, "/Subscriber")
api.add_resource(Children, "/Child")
api.add_resource(Reports, "/Reports")
api.add_resource(Levels, "/Levels")
api.add_resource(SubjectData, "/SubjectData")
api.add_resource(Activity, "/Activity")
api.add_resource(DownloadActivity, "/DownloadActivity")
api.add_resource(States, "/States")
api.add_resource(Subjects, "/Subjects")
api.add_resource(Webhook, "/Webhook")
api.add_resource(AIActivity, "/AIActivity")