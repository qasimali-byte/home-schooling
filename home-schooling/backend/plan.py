"""Modules"""
import json
from flask import jsonify
from flask_restful import Resource, reqparse, abort, request
from sentry_sdk import capture_exception
from flask_jwt_extended import get_jwt_identity
import stripe
from config import MySqlDatabase, CLIENT_SECRET , log_manager
from utils import jwt_required, role


class Plan(Resource):
    """Subscription Plans"""

    def __init__(self):
        
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()
        self.login_args = reqparse.RequestParser()
        self.login_args.add_argument(
            "email", type=str, help="email for Login", required=True
        )
        # Request arguments
        self.payment_args = reqparse.RequestParser()
        self.payment_args.add_argument(
            "email", type=str, help="email for stripe", required=True
        )
        self.payment_args.add_argument(
            "price_id", type=str, help="price id for payment", required=True
        )


    def get(self):
        """Plans route"""
        log_manager.log("success", "=== GET Plans API ===")
        
        # try except block for getting plans data from db
        try:
            self.cursor.execute("""SELECT * from plan where isActive=1""")
            plans = self.cursor.fetchall()

            if not plans:
                log_manager.log("info", "Successfully fetched. No plans found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No plans.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched plans : {plans[0]}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify(data=plans)

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting plans : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching plans")


    def patch(self):
        """Check mail"""
        log_manager.log("success", "=== PATCH Check email API ===")

        # try except block for API body parameters
        try:
            args = self.login_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in checking email")

        # try except block for checking user email
        try:
            
            self.cursor.execute(
                """SELECT email FROM user WHERE email=%s""", (args["email"],)
            )
            email = self.cursor.fetchone()
            if email:
                log_manager.log("warning", f"Email already exists : {args['email']}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")                
                response = jsonify(status=501, message="Email already exists")
                response.status_code = 501
                return response

            return jsonify(status=200)

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error checking email: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================") 
            abort(http_status_code=501, message="Error in checking email")


    def post(self):
        """Subscription Plans"""
        log_manager.log("success", "=== POST Subscription plan creation API ===")

        # try except block for API body parameters
        try:
            args = self.payment_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding subscription plan")

        # try except block for creating payment intent
        try:
           
            stripe.api_key = CLIENT_SECRET

            customer = stripe.Customer.create(email=args["email"])
            
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    'price': args["price_id"] ,
                }],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )


            log_manager.log("info", "Payment subscription created Successfully")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({
                "customer_id" : customer.id,
                "subscriptionId" : subscription.id, 
                "clientSecret": subscription.latest_invoice.payment_intent.client_secret
            })

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in creating payment intent : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding subscription plan")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def delete(self):
        """Delete stripe subscription"""
        log_manager.log("success", "=== DELETE cancel stripe subscription API ===")

        # try except block for checking API search query params
        try:
            subscription_id = int(request.args.get("subscription_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting stripe subscription")
        

        # try except block to get stripe subscription id for this subscription
        try:
            self.cursor.execute(
                """SELECT stripe_subscription_id FROM subscriptions WHERE id=%s""", (subscription_id,)
            )
            stripe_id = self.cursor.fetchone()

            if not stripe_id:
                log_manager.log("info", "Successfully fetched. No stripe subscription found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No stripe subscription.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched stripe subscription : {stripe_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting stripe id from DB : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting stripe subscription")

        
        # try except block for cancelling fetched stripe subscription
        try:
            stripe.api_key = CLIENT_SECRET
            deleted_subscription = stripe.Subscription.delete(stripe_id["stripe_subscription_id"])
            log_manager.log("info", f"Successfully cancelled stripe subscription : {deleted_subscription}")

            self.cursor.execute("UPDATE subscriptions SET isActive = 0 WHERE id = %s", (subscription_id,))
            self.db.commit()
            log_manager.log("info", f"Successfully deactivated subscription : {subscription_id}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. Stripe subscription cancelled.",
                        "data": deleted_subscription,
                    }
                )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error cancelling subscription : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting stripe subscription")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):
        """Get subscriptions route"""
        log_manager.log("success", "=== PUT Get subscriptions for user API ===")

        # try except block for getting current user id
        try:
            identity = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting subscriptions")
      

        # try except block for getting active subscriptions
        try:
            self.cursor.execute(
                """
                SELECT 
                    subscriptions.*, 
                    plan.id as plan_id,
                    plan.duration AS plan_duration,
                    plan.price AS plan_price,
                    plan.isActive AS plan_isAcive,
                    plan.date_created AS plan_datecreated, 
                    plan.name AS plan_name,
                    plan.extra_data AS plan_extradata,
                    plan.stripe_id AS plan_stripeid
                FROM 
                    subscriptions
                INNER JOIN 
                    plan ON subscriptions.plan_id = plan.id
                WHERE 
                    subscriptions.user_id=%s AND subscriptions.isActive=1
                """,
                (identity,)
            )
            subscriptions = self.cursor.fetchall()

            if not subscriptions:
                log_manager.log("info", "Successfully fetched. No subscriptions found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No subscriptions.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched subscriptions : {subscriptions}.")
            for i in subscriptions:
                i['plan_extradata'] = json.loads(i['plan_extradata'])

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in fetching subscriptions : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting subscriptions")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": subscriptions
            }
        )


