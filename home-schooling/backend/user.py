"""Modules"""
from datetime import datetime
import datetime as dt
import json
from flask import jsonify
from flask_restful import Resource, reqparse, abort
from sentry_sdk import capture_exception
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
)
from config import MySqlDatabase, blacklist, log_manager, initialize_ai_for_user
from utils import jwt_required, role, send_email_verification
import threading


# ROUTES DEFINITIONS
class User(Resource):
    """User Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # Request arguments
        self.login_args = reqparse.RequestParser()
        self.login_args.add_argument(
            "email", type=str, help="email for Login", required=True
        )
        self.login_args.add_argument(
            "password", type=str, help="Password for Login", required=True
        )


        self.user_signup = reqparse.RequestParser()
        self.user_signup.add_argument(
            "first_name", type=str, help="first_name of user", required=True
        )
        self.user_signup.add_argument(
            "last_name", type=str, help="last_name of user", required=True
        )
        self.user_signup.add_argument(
            "email", type=str, help="email of user", required=True
        )
        self.user_signup.add_argument(
            "password", type=str, help="email of user", required=True
        )
        self.user_signup.add_argument(
            "address", type=str, help="address of user", required=True
        )
        self.user_signup.add_argument(
            "post_code", type=str, help="post_code of user", required=True
        )
        self.user_signup.add_argument(
            "plan_id", type=int, help="plan_id of user", required=True
        )
        self.user_signup.add_argument(
            "price", type=int, help="price of plan of user", required=True
        )
        self.user_signup.add_argument(
            "user_stripe_id", type=str, help="stripe id for user", required=True
        )
        self.user_signup.add_argument(
            "state_id", type=int, help="state id for child", required=True
        )
        self.user_signup.add_argument(
            "stripe_subscription_id", type=str, help="stripe id for subcsription", required=True
        )



    def post(self):
        """User Login Routes"""
        log_manager.log("success", "=== POST User login API ===")

        # try except block for API body parameters
        try:
            args = self.login_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while login")

        email = args["email"]
        password = args["password"]

        try:
            # retrieving hashed password from db to compare
            self.cursor.execute(
                """SELECT id, password, isActive FROM user WHERE email=%s""",
                (email,),
            )
            user = self.cursor.fetchone()

            if not user:
                message = "Incorrect Email or Password. Try Again!"
                log_manager.log("error", f"{message} - Email : {email}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response

            if user["isActive"] == 0:
                message = "Email not verified"
                log_manager.log("warning", f"{message} : {email} ")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response


            if check_password_hash(user["password"], password):
                self.cursor.execute("SET sql_mode = ''")
                self.cursor.execute(
                            """SELECT COUNT(*) AS sub_count FROM subscriptions WHERE user_id=%s AND isActive=1""",
                            (user["id"],),
                        )
                user_subscription = self.cursor.fetchone()
                subscription_count = user_subscription['sub_count']
                if subscription_count == 0:
                    message = "User does not have an active subscription"
                    log_manager.log("warning", message)
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    response = jsonify(status=406, message=message)
                    response.status_code = 200
                    return response

                # returning access, refresh token
                expires = dt.timedelta(days=1)
                access_token = create_access_token(
                    identity=str(user["id"]),
                    additional_claims={"role": "User"},
                    expires_delta=expires,
                )

                refresh_token = create_refresh_token(
                    identity=str(user["id"]), additional_claims={"role": "User"}
                )


                log_manager.log("info", f"User logged in with email : {email} ")
                
                # calling thread function in utils.py to get elaborations for this user only 
                threading.Thread(target=initialize_ai_for_user, args=(user["id"],)).start()

                return jsonify(
                    {
                        "status": 200,
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                )
        
            message = "Incorrect Email or Password. Try Again!"
            log_manager.log("error", f"{message} - Email : {email}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            response = jsonify(status=501, message=message)
            response.status_code = 501
            return response

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in login : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while login")


    def patch(self):
        """User Signup Route"""
        log_manager.log("success", "=== PATCH User signup API ===")

        # try except block for API body parameters
        try:
            args = self.user_signup.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while signup")


        # try except block for user checking
        try:
            self.cursor.execute(
                """SELECT email FROM user WHERE email=%s""", (args["email"],)
            )
            email = self.cursor.fetchone()

            if email:
                message = "Email already exists"
                log_manager.log("warning", f"{message} - Email : {args['email']}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error checking existing email from DB : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while signup")


        # try except block for inserting user into db
        try:
            pass_hash = generate_password_hash(args["password"])
            self.cursor.execute(
                """INSERT INTO user (first_name,last_name,address,post_code,email,password,date_created,isActive,user_stripe_id,states_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    args["first_name"],
                    args["last_name"],
                    args["address"],
                    args["post_code"],
                    args["email"],
                    pass_hash,
                    datetime.today(),
                    0,
                    args["user_stripe_id"],
                    args["state_id"],
                ),
            )
            self.db.commit()
            user_id = self.cursor.lastrowid
            user_data_entered = {
                "id" : user_id,
                "first_name": args["first_name"],
                "last_name": args["last_name"],
                "address": args["address"],
                "post_code": args["post_code"],
                "email": args["email"],
                "date_created": datetime.today(),
                "isActive": 0,
                "user_stripe_id" : args["user_stripe_id"],
                "states_id": args["state_id"]
            }

            log_manager.log("info", f"User added in DB with data : {user_data_entered}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error inserting user data: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while signup")


        # try except block for subscriptions user into db
        try:
            self.cursor.execute(
                """INSERT INTO subscriptions(isActive,date_created,stripe_subscription_id,user_id,plan_id) 
                    VALUES (%s,%s,%s,%s,%s)""",
                (1, datetime.today(), args["stripe_subscription_id"], user_id, args["plan_id"], ),
            )
            self.db.commit()
            subscription_id = self.cursor.lastrowid

            subscription_data_entered = {
                "id" : subscription_id,
                "isActive" : 1,
                "date_created" : datetime.today(),
                "stripe_subscription_id" : args["stripe_subscription_id"],
                "user_id" : user_id,
                "plan_id" : args["plan_id"],
            }
            log_manager.log("info", f"Subscription added in DB with data : {subscription_data_entered}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error inserting subscription data: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while signup")


        # try except block for invoice user into db
        try:
            self.cursor.execute(
                """INSERT INTO invoice(subscription_id,price,date_created) VALUES (%s,%s,%s)""",
                (subscription_id, args["price"], datetime.today()),
            )
            self.db.commit()
            invoice_id = self.cursor.lastrowid
            invoice_data_entered = {
                "id" : invoice_id,
                "subscription_id" : subscription_id,
                "price" : args["price"],
                "date_created" : datetime.today()
            }

            log_manager.log("info", f"Invoice added in DB with data : {invoice_data_entered}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error inserting invoice data: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while signup")


        # try except block for sending email verification
        try:
            send_email_verification(args["email"], args["first_name"], user_id)
            log_manager.log("info", f"Verification email sent to email : {args['email']}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error sending email verification: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while signup")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", f"User Signup Successful with email : {args['email']}")
        return jsonify({"status": 200, "message": "User Signup Successful"})


    @role(refresh=True, user_role="User")
    @jwt_required(refresh=True)
    def get(self):
        """Refresh Token Routes"""
        log_manager.log("success", "=== Get Refresh tokens API ===")

        # try except block for getting curren user id
        try:
            identity = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in refreshing token")


        # try except block for creating access token
        try:
            expires = dt.timedelta(days=1)
            access_token = create_access_token(
                identity=identity, additional_claims={"role": "User"}, expires_delta=expires
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error creating access token: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in refreshing token")


        # try except block for creating refresh token
        try:
            refresh_token = create_refresh_token(
                identity=identity, additional_claims={"role": "User"}
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error creating refresh token: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in refreshing token")


        log_manager.log("info", "Successfully Generated tokens")
        return jsonify(
            {
                "status": 200,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):


        """User Logout Routes"""
        log_manager.log("success", "=== PUT User logout API ===")

        try:
            jti = get_jwt()["jti"]
            blacklist.add(jti)

            log_manager.log("info", "Successfully logged out")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Successfully logged out"})

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error logging out user : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in Logging out")