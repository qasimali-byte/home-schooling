"""Modules"""
from ast import literal_eval
import json
import math
from flask import jsonify
from flask_restful import Resource, reqparse, request,abort
from sentry_sdk import capture_exception
from config import MySqlDatabase,log_manager
from utils import (
    append_data, jwt_required, role, parse_code
)

# ROUTES DEFINITIONS
class Levels(Resource):
    """User Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()
        # Request arguments

    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """List levels from dump data Routes"""
        log_manager.log("success", "=== GET level API ===")

        # try except block for getting level data
        try:
            query = """
                    SELECT 
                        level.id AS value ,
                        level.name AS label
                    FROM 
                        level
                    """

            query += " ORDER BY level.id ASC"

            self.cursor.execute(query)
            levels = self.cursor.fetchall()

            if not levels:
                log_manager.log("info", "Successfully fetched. No levels found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No levels.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched {len(levels)} levels : {levels[0]}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting levels : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching levels")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": levels
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """Get codes by subject from non term report activities API"""
        log_manager.log("success", "=== POST get CdCodes for non term report subject API ===")

        # try except block for checking query params
        try:
            page_size, page_number, report_id, subject_id = (
                int(request.args.get("page_size")),
                int(request.args.get("page_number")),
                int(request.args.get("report_id")),
                int(request.args.get("subject_id")),
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching non-term report subject codes")

        # try except block for fetching codes by subject
        try:
            query = """
                SELECT
                    	subject.name AS subject_name,
                        learning.name AS learning_name,
                        TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(REPLACE(json_subject_data, "'", ''), '"', ''), '{', ''), '}', ''), 'CdCode:', -1), ',', 1)) AS CdCode,
                        TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(REPLACE(json_subject_data, "'", ''), '"', ''), '{', ''), '}', ''), 'Strand:', -1), ',', 1)) AS strand_name,
                        TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(REPLACE(json_subject_data, "'", ''), '"', ''), '{', ''), '}', ''), 'Substrand:', -1), ',', 1)) AS sub_strand_name
                FROM 
                    home_schooling.activites
                INNER JOIN 
                    subject ON activites.subject_id = subject.id
                INNER JOIN 
                    learning ON subject.learning_id = learning.id
                WHERE 
                    report_id = %s AND subject_id = %s
                GROUP BY
                    CdCode, strand_name, sub_strand_name
                LIMIT %s OFFSET %s
            """

            val = []
            val.append(report_id)
            val.append(subject_id)
            val.append(page_size)
            val.append(page_number)
            val = tuple(val)
            
            self.cursor.execute(query, val)
            subject_data = self.cursor.fetchall()
            for item in subject_data:
                for key, value in item.items():
                    if isinstance(value, bytes):
                        item[key] = value.decode('utf-8')

            if not subject_data:
                log_manager.log("info", "Successfully fetched. No unique codes for non-term report subject.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No unique codes.",
                        "data": [],
                    }
                )


            log_manager.log("info", f"Successfully fetched unique codes for non-term report subject : {subject_data[0]}.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting codes by subject: {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching non-term report subject codes")


        # try except block for getting counts
        try:
            count_query = """
                SELECT COUNT(*) AS total_records
                FROM (
                    SELECT
                        SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'CdCode': '", -1), "',", 1) AS CdCode,
                        SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Strand': '", -1), "',", 1) AS strand_name,
                        SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Substrand': '", -1), "',", 1) AS sub_strand_name
                    FROM 
                        home_schooling.activites
                    WHERE 
                        report_id = %s AND subject_id = %s
                    GROUP BY
                        CdCode, strand_name, sub_strand_name
                ) AS subquery
            """
            self.cursor.execute(count_query, val[:-2])
            total_records = self.cursor.fetchone()["total_records"]
            pages = math.ceil(total_records / page_size)

            log_manager.log("info", f"Successfully fetched {total_records} non-term report subject codes ")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting codes count by subject: {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching non-term report subject codes")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successful",
                "data": subject_data,
                "total_records": total_records,
                "pages": pages,
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):
        """Get codes by subject from non term report activities API"""
        log_manager.log("success", "=== POST get CdCodes for non term report subject API ===")

        # try except block for checking query params
        try:
            page_size, page_number, report_id, term_id = (
                int(request.args.get("page_size")),
                int(request.args.get("page_number")),
                int(request.args.get("report_id")),
                request.args.get("term_id"),
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching term report subject codes")

        # try except block for fetching codes by subject
        try:
            query = """
                SELECT
                    subject.id AS subject_id,
                    subject.name AS subject_name,
                    learning.name AS learning_name,
                    SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'CdCode': '", -1), "',", 1) AS CdCode,
                    SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Strand': '", -1), "',", 1) AS strand_name,
                    SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Substrand': '", -1), "',", 1) AS sub_strand_name"""
            
            if term_id:
                query += """
                    ,states_has_terms.terms_id AS term_id
                """
            
            query += """
                FROM 
                    home_schooling.activites
                INNER JOIN
                    states_has_terms ON activites.states_has_terms_id = states_has_terms.terms_id
                INNER JOIN 
                    subject ON activites.subject_id = subject.id
                INNER JOIN
                    learning ON subject.learning_id = learning.id
            """

            where_conditions = []
            val = []

            where_conditions.append(" activites.report_id=%s ")
            val.append(report_id)

            if term_id:
                where_conditions.append(" states_has_terms.terms_id=%s")
                val.append(int(term_id))

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

            query += """
                GROUP BY
                    CdCode, learning_name, strand_name, sub_strand_name, subject_id"""
            if term_id : 
                query += """, term_id ORDER BY term_id"""
            
            count_query = query
            query += """ LIMIT %s OFFSET %s """

            val.append(page_size)
            val.append(page_number)
            val = tuple(val)
            print(query)
            self.cursor.execute(query, val)
            subject_data = self.cursor.fetchall()

            for item in subject_data:
                for key, value in item.items():
                    if isinstance(value, bytes):
                        item[key] = value.decode('utf-8')

            if not subject_data:
                log_manager.log("info", "Successfully fetched. No unique codes for term report.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No unique codes.",
                        "data": [],
                    }
                )


            log_manager.log("info", f"Successfully fetched unique codes for term report : {subject_data[0]}.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting codes by term report subject : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching term report subject codes")


        # try except block for getting counts
        try:
            count_query_new = f""" SELECT COUNT(*) AS total_records FROM ({count_query}) AS subquery """
            print(count_query_new)
            self.cursor.execute(count_query_new, val[:-2])
            total_records = self.cursor.fetchone()["total_records"]
            pages = math.ceil(total_records / page_size)

            log_manager.log("info", f"Successfully fetched {total_records} term report subject codes ")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting codes count by term report subject : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching term report subject codes")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successful",
                "data": subject_data,
                "total_records": total_records,
                "pages": pages,
            }
        )



# ROUTES DEFINITIONS
class SubjectData(Resource):
    """User Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()
        # Request arguments


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def patch(self):
        """List learning,subject from dump data Routes"""
        log_manager.log("success", "=== PATCH List areas,subject for level API ===")

        # try except block for checking level id
        try:
            level_id = int(request.args.get("level_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing level_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching level data")


        # try except block for getting areas and subject for level id
        try:
            query = """
                SELECT
                    level.id AS level_id,
                    level.name AS level_name,
                    learning.id AS learning_id,
                    learning.name AS learning_name,
                    subject.id AS subject_id,
                    subject.name AS subject_name
                FROM 
                    level
                JOIN 
                    learning ON level.id = learning.level_id
                JOIN 
                    subject ON learning.id = subject.learning_id
                WHERE 
                    level.id = %s
                ORDER BY
                    level.name, learning.name, subject.name
            """
            self.cursor.execute(query , (level_id,))
            levels_data  = self.cursor.fetchall()

            if not levels_data:
                log_manager.log("info", "Successfully fetched. No level data found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No level data.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched levels data : {levels_data[0]}.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting levels data : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching level data")


        # try except block for data formatting of levels
        try:
            formatted_data = []

            for row in levels_data:
                learning_id = row['learning_id']
                learning_name = row['learning_name']
                subject_id = row['subject_id']
                subject_name = row['subject_name']

                found_learning = False
                for i, learning in enumerate(formatted_data):
                    if learning["value"] == learning_id:  # Changed "learning_id" to "value"
                        learning["subjects"].append({"value": subject_id, "label": subject_name})
                        found_learning = True
                        break

                if not found_learning:
                    formatted_data.append({
                        "value": learning_id,  # Changed "learning_id" to "value"
                        "label": learning_name,  # Changed "learning_name" to "label"
                        "subjects": [{"value": subject_id, "label": subject_name}],
                    })

            log_manager.log("info", f"Successfully formatted levels data.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error formatting levels data : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching level data")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": formatted_data
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):
        """List strand substrand from dump data Routes"""
        log_manager.log("success", "=== PUT List strand, substrand for subject API ===")

        # try except block for checking subject id
        try:
            subject_id = int(request.args.get("subject_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing subject_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching subjects data")


        # try except block for getting subject data for subject id
        try:
            query = """
                SELECT
                    json_data,
                    subject.name as subject_name
                FROM
                    subject_data
                JOIN
                    subject ON subject_data.subject_id = subject.id
                WHERE
                    subject_data.subject_id = %s
            """
            self.cursor.execute(query , (subject_id,))
            subject_data  = self.cursor.fetchall()

            if not subject_data:
                log_manager.log("info", "Successfully fetched. No subject data found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No subject data.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched levels data : {subject_data[0]}.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting subjects data : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching subjects data")
        

        # try except block for data formatting of strand substrand data
        try:
            formatted_data = []

            for item in subject_data:
                parsed_data = json.loads(item["json_data"])

                strand = parsed_data.get("Strand")
                sub_strand = parsed_data.get("Substrand")

                strand_exists = any(item["Strand"] == strand for item in formatted_data)

                if not strand_exists:
                    formatted_item = {
                        "Strand": strand,
                        "Sub_strands": [],
                    }
                    if sub_strand:
                        formatted_item["Sub_strands"].append(sub_strand)
                    formatted_data.append(formatted_item)

                else:
                    formatted_item = next(item for item in formatted_data if item["Strand"] == strand)
                    if sub_strand and sub_strand not in formatted_item["Sub_strands"]:
                        formatted_item["Sub_strands"].append(sub_strand)

            log_manager.log("info", f"Successfully formatted subjects data.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error formatting levels data : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching subjects data")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": formatted_data
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """List codes for subject-strand-substrand from dump data route"""
        log_manager.log("success", "=== GET codes and data for subject-strand-substrand API ===")

        # try except block for checking API search query params
        try:
            subject_id, strand_name, substrand_name = (
                int(request.args.get("subject_id")),
                request.args.get("strand_name"),
                request.args.get("substrand_name"),
            )
        
        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting codes data")


        # try except block for getting json data for subject-strand-substrand
        try:
            query = """
                SELECT
                    json_data
                FROM
                    subject_data
                WHERE
                    subject_data.subject_id = %s
                    AND JSON_EXTRACT(json_data, '$.Strand') = %s
                    AND JSON_EXTRACT(json_data, '$.Substrand') = %s
                ORDER BY
                    JSON_EXTRACT(json_data, '$.CdCode') ASC
            """
            self.cursor.execute(query , (subject_id, strand_name, substrand_name))
            json_data  = self.cursor.fetchall()
            
            if not json_data:
                log_manager.log("info", f"Successfully fetched. No json data for subject {subject_id}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No json data found",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched json data for subject_id : {subject_id}")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting unique subjects : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching unique subjects")


        # try except block for formatting json data for subject-strand-substrand
        try:
            formatted_data = []

            for row in json_data:
                parsed_data = json.loads(row['json_data'])
                code = parsed_data.get("CdCode")

                existing_entry = next((item for item in formatted_data if item["code"] == code), None)
                if existing_entry:
                    append_data(existing_entry, parsed_data)
                else:
                    formatted_item = parse_code(parsed_data)
                    formatted_data.append(formatted_item)

            log_manager.log("info", f"Successfully formatted JSON data.")


        except Exception as e:
            capture_exception(e)
            error_message = f"Error formatting JSON data : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in formatting JSON data")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": formatted_data
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """List unique subject for report from activities Routes"""
        log_manager.log("success", "=== POST List unique subjects for report API ===")

        # try except block for checking report id
        try:
            report_id = int(request.args.get("report_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing report_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching unique subjects")


        # try except block for getting unique subjects for report id
        try:
            query = """
                SELECT DISTINCT
                    activites.subject_id,
                    subject.name AS subject_name
                FROM
                    activites
                JOIN
                    subject ON activites.subject_id = subject.id    
            """
                        
            where_conditions = []
            val = []

            where_conditions.append(" activites.report_id=%s ")
            val.append(report_id)

            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            
            self.cursor.execute(query , (report_id,))
            subjects  = self.cursor.fetchall()
            
            if not subjects:
                log_manager.log("info", f"Successfully fetched. No unique subjects for report : {report_id}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No unique subjects",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched unique subjects : {subjects[0]}.")

        except Exception as e:
            capture_exception(e)
            error_message = f"Error getting unique subjects : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching unique subjects")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": subjects
            }
        )


