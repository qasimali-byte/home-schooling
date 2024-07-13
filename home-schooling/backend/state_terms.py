"""Modules"""
from flask import  jsonify
from flask_restful import Resource, reqparse,abort
from sentry_sdk import capture_exception
from config import MySqlDatabase,log_manager
from utils import jwt_required, role


# ROUTES DEFINITIONS
class States(Resource):
    """State Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # Request arguments
        self.state_term_args = reqparse.RequestParser()
        self.state_term_args.add_argument(
            "report_id", type=int, help="id of report to get ranges", required=True
        )

    def get(self):
        """List state Routes"""
        log_manager.log("success", "=== GET states API ===")

        try:
            self.cursor.execute("""SELECT * from states""")
            states = self.cursor.fetchall()

            log_manager.log("info", f"Successfully fetched states : {states}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify(
                {
                    "status": 200,
                    "message": "Request was successful",
                    "data": states,
                }
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting states : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching states")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)    
    def post(self):
        """Get date ranges for a report"""
        log_manager.log("success", "=== POST get date ranges for report id API ===")

        # try except block for checking report id
        try:
            args = self.state_term_args.parse_args()
            report_id = int(args['report_id'])
        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing report_id: {e}")
            abort(http_status_code=501, message="Error in fetching date ranges")


        # try except block for getting date ranges
        try:
            query = """
                    SELECT
                        report.id AS report_id,
                        child.id AS child_id,
                        CONCAT(child.first_name, ' ', child.last_name) AS child_name,
                        states.id AS state_id,
                        states.name AS state_name,
                        states_has_terms.id as state_terms_id,
                        states_has_terms.terms_id as term_id,
                        terms.name as term_name,
                        states_has_terms.start_date AS term_start_date,
                        states_has_terms.end_date AS term_end_date
                    FROM
                        report 
                    JOIN
                        child ON report.child_id = child.id
                    JOIN
                        states ON child.states_id = states.id
                    JOIN
                        states_has_terms ON states.id = states_has_terms.states_id
                    JOIN
                        terms ON states_has_terms.terms_id = terms.id
                    WHERE
                        report.id = %s;
                    """

            self.cursor.execute(query, (report_id,))
            date_ranges = self.cursor.fetchall()

            log_manager.log("info", f"Successfully fetched date ranges for report {report_id} : {date_ranges}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting date ranges : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching date ranges")


        result = {
            'report_id': None,
            'child_id': None,
            'child_name': None,
            'state_id': None,
            'state_name': None,
            'date_ranges': []
        }

        for row in date_ranges:
            if result['report_id'] is None:
                result['report_id'] = row['report_id']
                result['child_id'] = row['child_id']
                result['child_name'] = row['child_name']
                result['state_id'] = row['state_id']
                result['state_name'] = row['state_name']

            result['date_ranges'].append({
                'state_terms_id': row['state_terms_id'],
                'term_id': row['term_id'],
                'term_name': row['term_name'],
                'term_start_date': row['term_start_date'],
                'term_end_date': row['term_end_date']
            })

        log_manager.log("info", f"Successfully date ranges for report {report_id} : {result['date_ranges'][0]}.")
        return jsonify(data=result)
