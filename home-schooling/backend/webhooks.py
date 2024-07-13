"""Modules"""
import json
from flask import jsonify
from flask_restful import Resource, reqparse, abort, request
import stripe
from sentry_sdk import capture_exception
from config import MySqlDatabase, CLIENT_SECRET , log_manager,WEBHOOK_SECRET
from utils import send_subscription_fail_email


# ROUTES DEFINITIONS
class Webhook(Resource):
    """Strip Webhook"""

    def __init__(self):
        
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()
        self.webhook_args = reqparse.RequestParser()
       

    def post(self):
        """Webhook for failed invoice payment"""
        log_manager.log("success", "=== POST check failed payment Webhook ===")

        request_data = json.loads(request.data)

        if WEBHOOK_SECRET:
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=WEBHOOK_SECRET)
                data = event['data']
            except Exception as e:
                return e
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']

        data_object = data['object']

        
        if event_type == 'invoice.payment_failed':
            
            # try except block for getting customer id
            try:
                customer_id = data_object.get('customer')
                log_manager.log("info", f"Fetched customer id from event object : {customer_id}")
        
            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error getting customer id from event object : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error while executing webhook for payment failure")


            # try except block for getting user data from DB
            try:
                query = "SELECT id,email,concat(first_name,' ',last_name) AS user_name FROM user WHERE user_stripe_id = %s"
                self.cursor.execute(query, (customer_id,))
                user = self.cursor.fetchone()

                if not user:
                    log_manager.log("info", "Successfully fetched. No user found.")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    return jsonify(
                        {
                            "status": 200,
                            "message": "Request was successful. No user.",
                            "data": [],
                        }
                    )

                user_id = user.get('id')
                user_email  = user.get('email')
                user_name  = user.get('user_name')
                log_manager.log("info", f"Fetched user from db for customer id : {user}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error getting user data : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error while executing webhook for payment failure")


            # try except block for updating user subscription
            try:
                update_query = "UPDATE subscriptions SET isActive = 0 WHERE user_id = %s"
                self.cursor.execute(update_query, (user_id,))
                self.db.commit()

                log_manager.log("info", f"Subscription deactivated for user with ID: {user_id}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error updating subscription for user : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error while executing webhook for payment failure")


            # try except block for sending invalid payment email
            try:
                send_subscription_fail_email(user_email ,user_name)
                log_manager.log("info", f"Subscription deactivated for user with ID: {user_id}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error sending email : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error while executing webhook for payment failure")

        
        return jsonify({'status': 'success'})
       