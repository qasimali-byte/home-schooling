"""Modules"""
import math
from datetime import date
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, reqparse, request,abort
from sentry_sdk import capture_exception
from config import MySqlDatabase,log_manager
from utils import jwt_required, role


# ROUTES DEFINITIONS
class Reports(Resource):
    """Report Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # Request arguments
        self.report_args = reqparse.RequestParser()
        self.report_args.add_argument(
            "name", type=str, help="name of report", required=True
        )
        self.report_args.add_argument(
            "follow_term", type=bool, help="report follow terms or not", required=True
        )
        self.report_args.add_argument(
            "child_id", type=int, help="child linked to report", required=True
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """List reports Routes"""
        log_manager.log("success", "=== GET reports API ===")
        
        # try except block for checking API search query params
        try:
            page_size, page_number, search = (
                int(request.args.get("page_size")),
                int(request.args.get("page_number")),
                request.args.get("search"),
            )
        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching reports")


        # try except block for checking user identity
        try:
            current_user = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching reports")


        # try except block for getting reports data
        try:
            query = """
                    SELECT
                        report.id,
                        report.name,
                        report.create_date,
                        report.last_edited,
                        report.follow_term,
                        child.id as child_id,
                        CONCAT(child.first_name, ' ', child.last_name) AS child_name,
                        states.name AS state_name,
                        level.name AS level_name,
                         level.id AS level_id
                    FROM 
                        report
                    JOIN 
                        child ON report.child_id = child.id
                    JOIN
                        user ON child.user_id = user.id
                    JOIN
                        states ON child.states_id = states.id
                    JOIN
                        level ON child.level_id = level.id
                    """

            where_conditions = []
            val = []
            if search:
                search = "%" + search.lower() + "%"
                where_conditions.append("LOWER(report.name) LIKE %s ")
                val.append(search)

            if current_user:
                where_conditions.append(" child.user_id = %s ")
                val.append(current_user)

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

            query += " ORDER BY report.id DESC LIMIT %s OFFSET %s"

            val.append(page_size)
            val.append(page_number)
            val = tuple(val)

            self.cursor.execute(query, val)
            report = self.cursor.fetchall()

            if not report:
                log_manager.log("info", "Successfully fetched. No reports found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No date ranges.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched reports : {report[0]}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting reports : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching reports")


        # try except block for getting reports count
        try:
            query_count = """
                            SELECT COUNT(*) AS total_records 
                            FROM report 
                            JOIN child ON report.child_id = child.id"""

            if where_conditions:
                query_count += " WHERE " + " AND ".join(where_conditions)

            self.cursor.execute(query_count, val[:-2])
            total_records = self.cursor.fetchone()["total_records"]
            pages = math.ceil(total_records / page_size)
            log_manager.log("info", f"Successfully fetched reports count : {total_records}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting reports count : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching reports")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successful",
                "data": report,
                "total_records": total_records,
                "pages": pages,
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """Add Report Route"""
        log_manager.log("success", "=== POST add report API ===")

        # try except block for API body parameters
        try:
            args = self.report_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding report")


        # try except block for inserting report data into db
        try:
            current_date = date.today()
            self.cursor.execute(
                """INSERT INTO report (name,create_date,last_edited,follow_term,child_id) VALUES (%s,%s,%s,%s,%s)""",
                (
                    args["name"],
                    current_date,
                    current_date,
                    args["follow_term"],
                    args["child_id"],
                ),
            )
            self.db.commit()
            report_id = self.cursor.lastrowid
            log_manager.log("info", f"Report added in DB with id : {report_id} - data : {args}")
            
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Report added Successful"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error adding report: {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding report")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def patch(self):
        """Edit report Routes"""
        log_manager.log("success", "=== PATCH edit report API ===")

        # try except block for API body parameters
        try:
            self.report_args.remove_argument("child_id")
            args = self.report_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing report")


        # try except block for checking report id
        try:
            report_id = int(request.args.get("report_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing report_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing report")


        # try except block for editing report query
        try:
            self.cursor.execute(
                "UPDATE report set name=%s where report_id=%s", (args["name"], report_id)
            )

            self.db.commit()
            log_manager.log("info", f"Report edited in DB with id : {report_id} - data : {args}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Report Edited Successfully"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error editing report: {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing report")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def delete(self):
        """Delete Report"""
        log_manager.log("success", "=== DELETE report API ===")

        # try except block for checking report id
        try:
            report_id = int(request.args.get("report_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing report_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting report")


        # try except block for deleting report query
        try:
            query = """delete from report where id=%s"""
            self.cursor.execute(query, (report_id,))
            self.db.commit()

            log_manager.log("info", f"Report deleted with id : {report_id}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Report Deleted Successfully"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error deleting report: {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting report")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):
        """List subject, strands, sub-strands, and codes routes"""
        log_manager.log("success", "=== PUT view subject,strands,substrands & code API ===")

        # try except block for getting subject,strands,substrands & code data
        try:
            self.cursor.execute(
                """
                SELECT
                    subject.id AS subject_id,
                    subject.name AS subject_name,
                    strand.id AS strand_id,
                    strand.name AS strand_name,
                    sub_strand.id AS sub_strand_id,
                    sub_strand.name AS sub_strand_name,
                    sub_strand_code.id AS sub_strand_code_id,
                    sub_strand_code.code,
                    sub_strand_code.description
                FROM
                    subject
                LEFT JOIN
                    strand ON subject.id = strand.subject_id
                LEFT JOIN
                    sub_strand ON strand.id = sub_strand.strand_id
                LEFT JOIN
                    sub_strand_code ON sub_strand.id = sub_strand_code.sub_strand_id
                ORDER BY
                    subject.id, strand.id, sub_strand.id, sub_strand_code.id;
            """
            )

            results = self.cursor.fetchall()

            if not results:
                log_manager.log("info", "Successfully fetched. No subject,strands,substrands & code found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No subject,strands,substrands & code.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched subject,strands,substrands & code.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting subject,strands,substrands & code : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching subject,strands,substrands & code")


        data = []

        for row in results:
            subject_data = next(
                (subj for subj in data if subj["subject_id"] == row["subject_id"]), None
            )

            if not subject_data:
                subject_data = {
                    "subject_id": row["subject_id"],
                    "subject": row["subject_name"],
                    "strands": [],
                }
                data.append(subject_data)

            strand_data = next(
                (
                    strand
                    for strand in subject_data["strands"]
                    if strand["strand_id"] == row["strand_id"]
                ),
                None,
            )

            if not strand_data:
                strand_data = {
                    "strand_id": row["strand_id"],
                    "strand": row["strand_name"],
                    "sub_strands": [],
                }
                subject_data["strands"].append(strand_data)

            sub_strand_data = next(
                (
                    sub_strand
                    for sub_strand in strand_data["sub_strands"]
                    if sub_strand["sub_strand_id"] == row["sub_strand_id"]
                ),
                None,
            )

            if not sub_strand_data:
                sub_strand_data = {
                    "sub_strand_id": row["sub_strand_id"],
                    "sub_strand_name": row["sub_strand_name"],
                    "codes": [],
                }
                strand_data["sub_strands"].append(sub_strand_data)

            code_data = {
                "sub_strand_code_id": row["sub_strand_code_id"],
                "code": row["code"],
                "description": row["description"],
            }

            sub_strand_data["codes"].append(code_data)

        log_manager.log("info", f"Successfully formatted subject,strands,substrands & code : {data[0]}.")

        return jsonify(
            {"status": 200, "message": "Request was successful", "data": data}
        )
