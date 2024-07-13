"""Modules"""
import math
from datetime import datetime
import datetime as dt
from flask import jsonify
from flask_restful import Resource, reqparse, request,abort
from flask_jwt_extended import (
    get_jwt_identity,
  
)
from sentry_sdk import capture_exception
from config import MySqlDatabase,log_manager, initialize_ai_for_user
from utils import jwt_required, role
import threading


# ROUTES DEFINITIONS
class Children(Resource):
    """User Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()
        # Request arguments
        self.child_args = reqparse.RequestParser()
        self.child_args.add_argument(
            "first_name", type=str, help="first_name of child", required=True
        )
        self.child_args.add_argument(
            "last_name", type=str, help="last_name of child", required=True
        )
        self.child_args.add_argument(
            "address", type=str, help="address of child", required=True
        )
        self.child_args.add_argument(
            "post_code", type=str, help="post_code of child", required=True
        )
        self.child_args.add_argument(
            "age", type=str, help="email of child", required=True
        )
        self.child_args.add_argument(
            "start_date", type=str, help="start_date of child", required=True
        )
        self.child_args.add_argument(
            "state_id", type=int, help="state id for child", required=True
        )
        self.child_args.add_argument(
            "level_id", type=int, help="level id for child", required=True
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """Add  Child Route"""
        log_manager.log("success", "=== POST add child API ===")


        # try except block for API body parameters
        try:
            args = self.child_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding child")


        # try except block for checking user identity
        try:
            user_id = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting user")


        # try except block for inserting child data into db
        try:
            self.cursor.execute(
                """INSERT INTO child (first_name,last_name,address,post_code,age,start_date,user_id,states_id,level_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    args["first_name"],
                    args["last_name"],
                    args["address"],
                    args["post_code"],
                    args["age"],
                    args["start_date"],
                    user_id,
                    args["state_id"],
                    args["level_id"],
                ),
            )
            self.db.commit()
            child_id = self.cursor.lastrowid
            log_manager.log("info", f"Child added in DB with id : {child_id} - data : {args}")

            # calling thread function in utils.py to get elaborations for this user only 
            threading.Thread(target=initialize_ai_for_user, args=(user_id,)).start()

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Child added Successful"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error adding child : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding child")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def patch(self):
        """Child Edit Route"""
        log_manager.log("success", "=== Patch edit child API ===")

        # try except block for API body parameters
        try:
            self.child_args.remove_argument("state_id")
            args = self.child_args.parse_args()
            user_id = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing child")


        # try except block for checking child id
        try:
            (child_id,) = (int(request.args.get("child_id")),)

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing child_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing child")


        # try except block for editing child query
        try:
            query = """Update child set first_name=%s, last_name=%s, address=%s, post_code=%s,age=%s, start_date=%s, level_id=%s where id=%s"""
            self.cursor.execute(
                query,
                (
                    args["first_name"],
                    args["last_name"],
                    args["address"],
                    args["post_code"],
                    args["age"],
                    args["start_date"],
                    args["level_id"],
                    child_id,
                ),
            )

            self.db.commit()
            log_manager.log("info", f"Child edited in DB with id : {child_id} - data : {args}")

            # calling thread function in utils.py to get elaborations for this user only 
            threading.Thread(target=initialize_ai_for_user, args=(user_id,)).start()

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Child Edited Successfully"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error editing child : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")            
            abort(http_status_code=501, message="Error in editing child")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """List Child Routes"""
        log_manager.log("success", "=== GET childs API ===")

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
            abort(http_status_code=501, message="Error in getting child")


        # try except block for checking user identity
        try:
            user_id = get_jwt_identity()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting JWT identity: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting user")


        # try except block for getting child data
        try:
            query = """
                    SELECT 
                        child.id AS id,
                        child.first_name,
                        child.last_name,
                        child.address,
                        child.post_code,
                        child.age,
                        child.start_date,
                        states.id AS state_id,
                        states.name AS state_name,
                        level.id AS level_id,
                        level.name AS level_name
                    FROM 
                        child 
                    JOIN 
                        states ON child.states_id = states.id
                    JOIN 
                        level ON child.level_id = level.id
                    WHERE user_id=%s
                    """

            where_conditions = []
            val = []
            val.append(user_id)

            if search:
                search = "%" + search.lower() + "%"
                where_conditions.append("LOWER(child.first_name) LIKE %s ")
                val.append(search)

            if where_conditions:
                query += "AND " + "".join(where_conditions)

            query += " ORDER BY child.id DESC LIMIT %s OFFSET %s"

            val.append(page_size)
            val.append(page_number)
            val = tuple(val)

            self.cursor.execute(query, val)
            child = self.cursor.fetchall()

            if not child:
                log_manager.log("info", "Successfully fetched. No child found.")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No childs.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched child : {child[0]}.")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting child : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching child")

        # try except block for getting child count
        try:
            query = """
                    SELECT COUNT(*) AS total_records 
                    FROM 
                        child 
                    JOIN 
                        states ON child.states_id = states.id
                    JOIN 
                        level ON child.level_id = level.id
                    WHERE user_id=%s 
                    """

            if where_conditions:
                query += "AND " + "".join(where_conditions)

            self.cursor.execute(query, val[:-2])
            total_records = self.cursor.fetchone()["total_records"]
            pages = math.ceil(total_records / page_size)
            log_manager.log("info", f"Successfully fetched child count : {total_records}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting child count : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching child")


        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify(
            {
                "status": 200,
                "message": "Request was successfull",
                "data": child,
                "total_records": total_records,
                "pages": pages,
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def delete(self):
        """Delete Child"""
        log_manager.log("success", "=== DELETE child API ===")

        # try except block for checking child id
        try:
            child_id = int(request.args.get("child_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing child_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting child")


        # try except block for deleting child query
        try:
            query = """delete from child where id=%s"""
            self.cursor.execute(query, (child_id,))
            self.db.commit()

            log_manager.log("info", f"Child deleted with id : {child_id}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Child Deleted Successfully"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error deleting child: {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting child")

