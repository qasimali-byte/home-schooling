"""Modules"""
from flask import jsonify
from flask_restful import Resource,reqparse,request,abort
from sentry_sdk import capture_exception
from werkzeug.security import check_password_hash,generate_password_hash
import jwt as libjwt
from jwt import ExpiredSignatureError
from flask_jwt_extended import (
    get_jwt_identity,
)
from config import MySqlDatabase,log_manager
from utils import jwt_required, role , send_welcome_email , send_plan_email
from api import app


class UserAccount(Resource):
    """User Account Details Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # Request arguments
        self.change_password_args = reqparse.RequestParser()
        self.change_password_args.add_argument("oldpassword", type=str,
                                            help="Old password for user", required=True)
        self.change_password_args.add_argument("newpassword", type=str,
                                            help="New password for user", required=True)
        self.change_password_args.add_argument("confirmPassword", type=str,
                                            help="Confirm new password for user", required=True)

        self.edit_profile = reqparse.RequestParser()
        self.edit_profile.add_argument("first_name", type=str,
                                            help="first_name for user", required=True)
        self.edit_profile.add_argument("last_name", type=str,
                                            help="last_name for user", required=True)
        self.edit_profile.add_argument("address", type=str,
                                            help="address for user", required=True)
        self.edit_profile.add_argument("state", type=int,
                                            help="state for user", required=True)
        self.edit_profile.add_argument("post_code", type=str,
                                            help="post_code for user", required=True)


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """User Account"""
        log_manager.log("success", "=== GET User API ===")

        # try except block for API body parameters
        try:
            self.change_password_args.remove_argument("oldpassword")
            self.change_password_args.remove_argument("newpassword")
            self.change_password_args.remove_argument("confirmPassword")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching user")


        # try except block for checking user identity
        try:
            user_id = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching user")


        # try except block for getting user data from db
        try:
            self.cursor.execute("""select * from user where id=%s""", (user_id,))
            user = self.cursor.fetchone()

            if not user:
                log_manager.log("info", "Successfully fetched. No user found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No users.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched user : {user}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")

            return jsonify(
                {
                    "status": 200,
                    "message": "Request was successful",
                    "data": user,
                }
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting users : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching user")

    
    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):
        """Password Change Route"""
        log_manager.log("success", "=== PUT password change API ===")

        # try except block for getting user identity
        try:
            user_id = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in changing password")


        # try except block for getting user data
        try:
            query = "select id,password from home_schooling.user where id=%s"
            val = (user_id,)
            self.cursor.execute(query, val)
            user = self.cursor.fetchone()

            if not user:
                message = "User not found."
                log_manager.log("warning", message)
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")                
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response
            
            log_manager.log("info", f"Successfully fetched user : {user}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting user data: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in changing password")


        # try except block for API body parameters
        try:
            args = self.change_password_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in changing password")

        oldpassword = args['oldpassword']
        password = args['newpassword']
        confirm_password = args['confirmPassword']

        # try except block for passowrd change
        try:

            if password and password != '':
                if confirm_password and confirm_password != '':
                    if confirm_password != password:
                        message = "Both Passwords Don't Match"
                        log_manager.log("warning", message)
                        MySqlDatabase.close_connection(self.cursor, self.db)
                        log_manager.log("info", "======================")
                        response = jsonify(status=501, message=message)
                        response.status_code = 501
                        return response

                else:
                    message = "Please enter a confirm password"
                    log_manager.log("warning", "Confirm password missing")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    response = jsonify(status=501, message=message)
                    response.status_code = 501
                    return response

            else:
                message = "Please enter a password"
                log_manager.log("warning", "Password missing")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response

            dbhasshedpassword = user['password']

            if check_password_hash(dbhasshedpassword, oldpassword):

                newhashedpassword = generate_password_hash(password)

                query = "UPDATE home_schooling.user set password=%s where id=%s"
                val = (newhashedpassword, user['id'])
                self.cursor.execute(query, val)
                self.db.commit()

                message = "PASSWORD CHANGED SUCCESSFULLY!!!!"
                log_manager.log("info", message)
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify({"status": 200, "message": message})

            message = "OLD PASSWORD IS WRONG"
            log_manager.log("warning", message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            response = jsonify(status=501, message=message)
            response.status_code = 501
            return response

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in changing password: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in changing password")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def patch(self):
        """Edit profile route"""
        log_manager.log("success", "=== PATCH Edit profile API ===")

        # try except block for API body parameters
        try:
            args = self.edit_profile.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in edit profile")


        # try except block for getting user identity
        try:
            user_id = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in edit profile")


        # try except block for getting user data
        try:

            self.cursor.execute(''' SELECT first_name, last_name, address, post_code FROM user WHERE user.id = %s ''', (user_id,))
            existing_user = self.cursor.fetchone()
            if not existing_user:
                message = "User doesn't exist"
                log_manager.log("warning", message)
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response

            log_manager.log("info", f"Successfully fetched user : {existing_user}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error fetching user data : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in edit profile")


        # try except block for updating user data
        try:

            self.cursor.execute("UPDATE user SET first_name=%s, last_name=%s, address=%s, post_code=%s, states_id=%s WHERE id=%s",
                                (args['first_name'], args['last_name'], args['address'], args['post_code'], args['state'], user_id))
            self.db.commit()

            user_data_updated = {
                "id" : user_id,
                "first_name": args['first_name'],
                "last_name": args['last_name'],
                "address": args['address'],
                "post_code": args['post_code'],
                "state" :  args['state'],
            }

            log_manager.log("info", f"User edited in DB with data : {user_data_updated}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "User Edited Successfully"})

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error editing user profile: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in edit profile")


    def post(self):
        """Setup email verification for User Routes"""
        log_manager.log("success", "=== POST Setup Email verification API ===")

        token=request.args.get('token')
        # try except block for checking session
        try:
            user=libjwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        except ExpiredSignatureError:            
            message="Your session has expired."
            log_manager.log("warning", message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=401, message=message)


        # try except block for getting user data
        try:
            query = "select id,email,first_name,isActive from user where id=%s"
            val = (user["sub"],)
            self.cursor.execute(query, val)
            user_check = self.cursor.fetchone()

            if not user_check:
                message = "User doesn't exist"
                log_manager.log("warning", message)
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response

            log_manager.log("info", f"Successfully fetched user : {user_check}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in fetching user data: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while Setup email verification")


        if user_check["isActive"] == 1:
            message="User already verified & active"
            log_manager.log("warning", message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify(status=200 , message=message)
        

        # try except block for sending welcome email
        try:
            send_welcome_email(user_check["email"],user_check["first_name"])
            log_manager.log("info", f"Welcome email sent at email : {user_check['email']}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error sending welcome email : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while Setup email verification")


        # try except block for updating user active status
        try:
            query = "UPDATE user set isActive=1 where id=%s"
            val = (user["sub"],)
            self.cursor.execute(query, val)
            self.db.commit()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error updating user status : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while Setup email verification")


        # try except block for getting subscription plan for activated user
        try:
            plan_query = """
                            SELECT 
                                subscriptions.user_id AS u_id, 
                                subscriptions.id AS s_id, 
                                subscriptions.plan_id AS p_id, 
                                plan.duration AS p_duration, 
                                plan.price  AS p_price, 
                                plan.name AS p_name
                            FROM subscriptions
                            JOIN plan ON subscriptions.plan_id = plan.id
                            WHERE subscriptions.user_id = %s
                            ORDER BY subscriptions.date_created DESC
                            LIMIT 1;
                        """
            plan_val=(user["sub"],)
            self.cursor.execute(plan_query,plan_val)
            plan_check=self.cursor.fetchone()

            if not plan_check:
                log_manager.log("info", "Successfully fetched. No plan found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No plan.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched plan for user id : {plan_val} : {plan_check}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", "Error Getting subscription plan for active user.")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while Setup email verification")


        # try except block for sending plan
        try:
            send_plan_email(user_check["email"],plan_check["p_name"],plan_check["p_duration"],plan_check["p_price"])
            log_manager.log("info", f"Plan email sent at email : {user_check['email']}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error sending plan email : {e}")
            MySqlDatabase.close_connection(self.cursor,self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while Setup email verification")


        log_manager.log("error", "Email verified successfully.")
        MySqlDatabase.close_connection(self.cursor,self.db)
        log_manager.log("info", "======================")
        return jsonify({"status":200,"message":"Email verified successfull. You can now login"})
