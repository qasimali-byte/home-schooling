"""Modules"""
import math
from flask import  jsonify
from flask_restful import Resource,request, reqparse,abort
from sentry_sdk import capture_exception
from config import MySqlDatabase, log_manager
from utils import jwt_required,  role


# ROUTES DEFINITIONS
class Subjects(Resource):
    """suject Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """List subject Routes"""
        log_manager.log("success", "=== GET subjects API ===")


        # try except block for checking API search query params
        try:
            report_id = int(request.args.get("report_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching unique subjects")


        # try except block for getting unique subjects for a report
        try:
            unique_subjects_query = """
                SELECT DISTINCT subject.id, subject.name
                FROM activites
                JOIN sub_strand_code ON activites.sub_strand_code_id = sub_strand_code.id
                JOIN sub_strand ON sub_strand_code.sub_strand_id = sub_strand.id
                JOIN strand ON sub_strand.strand_id = strand.id
                JOIN subject ON strand.subject_id = subject.id
                WHERE activites.report_id = %s;
            """
            self.cursor.execute(unique_subjects_query, (report_id,))
            unique_subjects = self.cursor.fetchall()

            if not unique_subjects:
                log_manager.log("info", "Successfully fetched. No unique subjects found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No unique subjects.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched subjects for report id : {report_id} - data : {unique_subjects}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")

            return jsonify(
                {
                    "status": 200,
                    "message": "Request was successful",
                    "data": unique_subjects,
                }
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting unique subjects : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching unique subjects")
    

    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """List subject strands Routes"""
        log_manager.log("success", "=== POST list subjects strands API ===")


        # try except block for checking API search query params
        try:
            page_size, page_number, report_id, subject_id,term_id , follow_term  = (
                int(request.args.get("page_size")),
                int(request.args.get("page_number")),
                int(request.args.get("report_id")),
                request.args.get("subject_id"),
                  request.args.get("term_id"),
                int(request.args.get("follow_term")),
               
            )


        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching subject strands")

        # if the user has decided not to follow terms, then we will show unique strand codes for one subject
        if follow_term == 0:

            # try except block for getting unique strand codes for a report
            try:
                unique_subjects_query = """
                    SELECT DISTINCT 
                        sub_strand_code.id as sub_strand_code_id, 
                         subject.id as subject_id,
                         strand.id as strand_id,
                        subject.name,strand.name as strand_name,
                        sub_strand_code.description,
                        sub_strand_code.code,
                        sub_strand.name as sub_strand_name,
                          sub_strand.id as sub_strand_id
                    FROM activites
                    JOIN sub_strand_code ON activites.sub_strand_code_id = sub_strand_code.id
                    JOIN sub_strand ON sub_strand_code.sub_strand_id = sub_strand.id
                    JOIN strand ON sub_strand.strand_id = strand.id
                    JOIN subject ON strand.subject_id = subject.id
                """

                where_conditions = []
                val = []

                if report_id:
                    where_conditions.append(" activites.report_id = %s ")
                    val.append(report_id)

                if subject_id:
                    where_conditions.append(" subject.id = %s ")
                    val.append(subject_id)

                if where_conditions:
                    unique_subjects_query += " WHERE " + " AND ".join(where_conditions)

                unique_subjects_query += " LIMIT %s OFFSET %s"

                val.append(page_size)
                val.append(page_number)
                val = tuple(val)

                self.cursor.execute(unique_subjects_query, val)
                unique_subjects_strands = self.cursor.fetchall()

                if not unique_subjects_strands:
                    log_manager.log("info", f"Successfully fetched. No strands found for follow_term : 0 - subject_id : {subject_id} - Report_id : {report_id}")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    return jsonify(
                        {
                            "status": 200,
                            "message": "Request was successful. No unique strands.",
                            "data": [],
                        }
                    )

                log_manager.log("info", f"Successfully fetched subjects strands for follow_term : 0 -  subject_id : {subject_id} - Report_id : {report_id} - data : {unique_subjects_strands[0]}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error getting unique strands : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error in fetching unique subjects")


            # try except block for getting unique strands count
            try:
                query_count = """
                        SELECT COUNT(DISTINCT sub_strand_code.id) AS total_records
                        FROM activites
                        JOIN sub_strand_code ON activites.sub_strand_code_id = sub_strand_code.id
                        JOIN sub_strand ON sub_strand_code.sub_strand_id = sub_strand.id
                        JOIN strand ON sub_strand.strand_id = strand.id
                        JOIN subject ON strand.subject_id = subject.id
                    """

                if where_conditions:
                    query_count += " WHERE " + " AND ".join(where_conditions)

                self.cursor.execute(query_count, val[:-2])
                total_records = self.cursor.fetchone()["total_records"]
                pages = math.ceil(total_records / page_size)
                log_manager.log("info", f"Successfully fetched unique strands count for follow_term : 0 -  subject_id : {subject_id} - Report_id : {report_id} : {total_records}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error getting unique strands count : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error in fetching reports")


            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify(
                {
                    "status": 200,
                    "message": "Request was successful",
                    "data": unique_subjects_strands,
                    "total_records": total_records,
                    "pages": pages,
                }
            )

        # if the user has decided to follow terms, then we will show unique strand codes for all subjects
        elif follow_term == 1:

            # try except block for getting unique subjects for a report
            try:
                unique_subjects_query = """
                    SELECT DISTINCT 
                        sub_strand_code.id as sub_strand_code_id, 
                        subject.name,
                         subject.id as subject_id,
                         strand.id as strand_id,
                        strand.name as strand_name,
                        sub_strand_code.description,
                        sub_strand_code.code,
                        sub_strand.id as sub_strand_id,
                        sub_strand.name as sub_strand_name
                    FROM activites
                    JOIN sub_strand_code ON activites.sub_strand_code_id = sub_strand_code.id
                    JOIN sub_strand ON sub_strand_code.sub_strand_id = sub_strand.id
                    JOIN strand ON sub_strand.strand_id = strand.id
                    JOIN subject ON strand.subject_id = subject.id
                """

                where_conditions = []
                val = []

                if report_id:
                    where_conditions.append(" activites.report_id = %s ")
                    val.append(report_id)

                if term_id:
                    where_conditions.append(" activites.states_has_terms_id = %s ")
                    val.append(term_id)

                if where_conditions:
                    unique_subjects_query += " WHERE " + " AND ".join(where_conditions)

                unique_subjects_query += " LIMIT %s OFFSET %s"

                val.append(page_size)
                val.append(page_number)
                val = tuple(val)

                self.cursor.execute(unique_subjects_query, val)
                unique_subjects_strands = self.cursor.fetchall()

                if not unique_subjects_strands:
                    # log_manager.log("info", f"Successfully fetched. No strands found for follow_term : 1 - term_id : {term_id} - Report_id : {report_id}")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    return jsonify(
                        {
                            "status": 200,
                            "message": "Request was successful. No unique strands.",
                            "data": [],
                        }
                    )

                # log_manager.log("info", f"Successfully fetched subjects strands for follow_term : 1 - term_id : {term_id} - Report_id : {report_id} - data : {unique_subjects_strands[0]}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error getting unique strands : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error in fetching unique subjects")


            # try except block for getting unique strands count
            try:
                query_count = """
                        SELECT COUNT(DISTINCT sub_strand_code.id) AS total_records
                        FROM activites
                        JOIN sub_strand_code ON activites.sub_strand_code_id = sub_strand_code.id
                        JOIN sub_strand ON sub_strand_code.sub_strand_id = sub_strand.id
                        JOIN strand ON sub_strand.strand_id = strand.id
                        JOIN subject ON strand.subject_id = subject.id
                    """

                if where_conditions:
                    query_count += " WHERE " + " AND ".join(where_conditions)

                self.cursor.execute(query_count, val[:-2])
                total_records = self.cursor.fetchone()["total_records"]
                pages = math.ceil(total_records / page_size)
                # log_manager.log("info", f"Successfully fetched unique strands count for follow_term : 1 - term_id : {term_id} - Report_id : {report_id} : {total_records}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error getting unique strands count : {e}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error in fetching reports")


            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify(
                {
                    "status": 200,
                    "message": "Request was successful",
                    "data": unique_subjects_strands,
                    "total_records": total_records,
                    "pages": pages,
                }
            )

        # if the user has given wrong follow_term input so we return error
        else:
            message = f"Wrong parameter given for follow_term "
            log_manager.log("error", message + f": {follow_term}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message=message)
