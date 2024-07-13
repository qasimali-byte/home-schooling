"""Modules"""
from datetime import date
from flask import jsonify
from flask_restful import Resource, reqparse, abort, request
from sentry_sdk import capture_exception
from config import MySqlDatabase,log_manager
from utils import send_subscription_renewal_email

class Subscriber(Resource):
    """Subscriptions"""

    def __init__(self):
        
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # Request arguments
        self.update_subscription_args = reqparse.RequestParser()
        self.update_subscription_args.add_argument(
            "email", type=str, help="email of user", required=True
        )
        self.update_subscription_args.add_argument(
            "stripe_subscription_id", type=str, help="stripe_subscription_id", required=True
        )
        self.update_subscription_args.add_argument(
            "plan_id", type=int, help="plan id linked", required=True
        )
        self.update_subscription_args.add_argument(
            "price", type=int, help="price of invoice", required=True
        )
        self.update_subscription_args.add_argument(
            "user_stripe_id", type=str, help="user_stripe_id", required=True
        )
        


    def post(self):
        """Subscription renewal Routes"""
        log_manager.log("success", "=== POST Subscription renewal API ===")

        # try except block for API body parameters
        try:
            args = self.update_subscription_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")


        # try except block for user checking
        try:
            self.cursor.execute(
                """SELECT id FROM user WHERE email=%s""", (args["email"],)
            )
            user = self.cursor.fetchone()
            if not user:
                message = "Email doesnt exists"
                log_manager.log("error", f"{message} - Email : {args['email']}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response

            user_id = user.get('id')
            log_manager.log("info", f"Fetched user with id : {user_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting user id by email : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")


        # try except block for updating user stripe id
        try:
            self.cursor.execute(
                """UPDATE user SET user_stripe_id = %s WHERE id = %s""",
                (args["user_stripe_id"], user_id)
            )
            self.db.commit()

            log_manager.log("info", f"User stripe id updated in DB for user : {user_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error updating user stripe id : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")
            

        # try except block for inserting subscriptions into db
        try:
            current_date = date.today()
            self.cursor.execute(
                """INSERT INTO subscriptions(isActive,date_created,stripe_subscription_id,user_id,plan_id) 
                    VALUES (%s,%s,%s,%s,%s)""",
                (1, current_date, args["stripe_subscription_id"], user_id, args["plan_id"], ),
            )
            self.db.commit()
            subscription_id = self.cursor.lastrowid

            log_manager.log("info", f"Subscription added in DB with data : {args}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error inserting subscription data : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")


        # try except block for invoice user into db
        try:
            self.cursor.execute(
                """INSERT INTO invoice(subscription_id,price,date_created) VALUES (%s,%s,%s)""",
                (subscription_id, args["price"], current_date),
            )
            self.db.commit()
            invoice_id = self.cursor.lastrowid

            log_manager.log("info", f"Invoice added in DB with id : {invoice_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error inserting invoice data : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")


        # try except block for getting relevant data from DB
        try:
            query = """
                SELECT 
                    plan.duration AS plan_duration,
                    plan.name AS plan_name
                FROM 
                    plan
                WHERE 
                    plan.id = %s;
            """
            self.cursor.execute(query, (args["plan_id"],))
            plan_data = self.cursor.fetchone()
            
            log_manager.log("info", f"Successfully fetched plan data : {plan_data}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error fetching plan data: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")


        # try except block for sending subscription renewal email
        try:
            send_subscription_renewal_email(args, plan_data)
            log_manager.log("info", f"Renewal email sent to email : {args['email']}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error sending renewal email: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error while subscription renewal")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify({"status": 200, "message": "Subscription renewed Successfully"})
