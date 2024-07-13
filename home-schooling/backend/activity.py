"""Modules"""
from collections import defaultdict
from datetime import date, datetime
import json
import math
from ast import literal_eval
from flask import jsonify
from flask_restful import Resource, reqparse, request, abort
from config import MySqlDatabase,log_manager
from sentry_sdk import capture_exception
from utils import (
    jwt_required,
    process_activities_for_subjects_view,
    role,
    generate_aws_signature_v4_post_urls,
)


# ROUTES DEFINITIONS
class Activity(Resource):
    """Activity Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # arguements for add activity
        self.activity_args = reqparse.RequestParser()
        self.activity_args.add_argument("start_date", type=str, help="start date of activity", required=True)
        self.activity_args.add_argument("end_date", type=str, help="end date of activity")
        self.activity_args.add_argument("description", type=str, help="description of activity", required=True)
        self.activity_args.add_argument("json_data", type=str, help="json_data of activity", required=True)
        self.activity_args.add_argument("urls",type=str,help="links for activity")
        self.activity_args.add_argument("file_names","--list",action="append",help="files for activity")
        self.activity_args.add_argument("report_id", type=int, help="report linked with activity", required=True)
        self.activity_args.add_argument("states_has_terms_id",type=int,help="state_term linked with activity")
        self.activity_args.add_argument("subject_id",type=int,help="subject id linked with activity",required=True)


        # arguements for attached files while editing
        self.files_args = reqparse.RequestParser()
        self.files_args.add_argument("description", type=str, help="description of activity", required=True)
        self.files_args.add_argument("json_data", type=str, help="json_data of activity", required=True)
        self.files_args.add_argument("urls",type=str,help="links for activity")
        self.files_args.add_argument("file_names","--list",action="append",help="file names for activity")
        self.files_args.add_argument("report_id", type=int, help="report linked with activity", required=True)
        self.files_args.add_argument("file_ids","--list",action="append",help="file ids for activity to be deleted")
        self.files_args.add_argument("subject_id",type=int,help="subject id linked with activity",required=True)


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """List activity Routes"""
        log_manager.log("success", "=== GET Activities API ===")

        # try except block for checking query params
        try:
            page_size, page_number, report_id, subject_id, CdCode, term_id, follow_term = (
                int(request.args.get("page_size")),
                int(request.args.get("page_number")),
                int(request.args.get("report_id")),
                int(request.args.get("subject_id")),
                request.args.get("CdCode"),
                request.args.get("term_id"),
                int(request.args.get("follow_term")),
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching activities")

        if follow_term not in [0, 1]:
            message = f"Wrong parameter given for follow_term "
            log_manager.log("error", message + f": {follow_term}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message=message)

        
        # try except block for getting activities for report
        try:

            # if the user has decided to follow terms, then we will show data grouped by date ranges
            if follow_term == 1:
                query = """
                    SELECT
                        activites.id as activity_id,
                        activites.act_start_date,
                        activites.act_end_date,
                        activites.description as activity_description,
                        activites.attached_links as attached_links,
                        activites.created_date ,
                        activites.inserted_date ,
                        activites.last_updated_date,
                        subject.id as subject_id,
                        subject.name as subject_name,
                        activites.json_subject_data,
                        states_has_terms.terms_id as term_id,
                        states_has_terms.id as states_has_terms_id,
                        concat('[',
                        GROUP_CONCAT(JSON_OBJECT('id', activity_files.id, 'file_name', activity_files.file_name)
                                ),']') as file_array    
                    FROM
                        activites
                    JOIN 
                        states_has_terms ON activites.states_has_terms_id = states_has_terms.id
                    LEFT JOIN 
                        activity_files ON activites.id = activity_files.activites_id AND activity_files.isDeleted = 0
                    JOIN
                        subject ON activites.subject_id = subject.id
                """

            # if the user has decided not to follow terms, then we will show data for subject selected
            elif follow_term == 0:
                query = """
                    SELECT
                        activites.id as activity_id,
                        activites.act_start_date,
                        activites.act_end_date,
                        activites.description as activity_description,
                        activites.attached_links as attached_links,
                        activites.created_date ,
                        activites.inserted_date ,
                        activites.last_updated_date,
                        subject.id as subject_id,
                        subject.name as subject_name,
                        activites.json_subject_data,
                        concat('[',
                        GROUP_CONCAT(JSON_OBJECT('id', activity_files.id, 'file_name', activity_files.file_name)
                                ),']') as file_array    
                    FROM 
                        activites
                    LEFT JOIN 
                        activity_files ON activites.id = activity_files.activites_id AND activity_files.isDeleted = 0
                    JOIN
                        subject ON activites.subject_id = subject.id
                """

            where_conditions = []
            val = []

            where_conditions.append(" activites.report_id=%s ")
            val.append(report_id)

            if follow_term ==1:
                if term_id:
                    where_conditions.append(" states_has_terms.terms_id=%s")
                    val.append(int(term_id))
            
            if subject_id:
                where_conditions.append(" activites.subject_id=%s")
                val.append(subject_id)
            
            if CdCode:
                
                where_conditions.append("SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, \"'CdCode': '\", -1), \"',\", 1) = %s")
                val.append(CdCode.strip())
            
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)

            if follow_term ==1:
                query += " group by activites.id ORDER BY activites.act_start_date DESC LIMIT %s OFFSET %s"
            
            elif follow_term == 0:
                query += " group by activites.id ORDER BY activites.id DESC LIMIT %s OFFSET %s"
            
            val.append(page_size)
            val.append(page_number)
            val = tuple(val)
            
            self.cursor.execute(query, val)
            activities = self.cursor.fetchall()

            if not activities:
                log_manager.log("info", f"Successfully fetched. No activities found for follow_term : {follow_term} - subject_id : {subject_id} - Report_id : {report_id}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")

                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No activities found for this report.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched activities for follow_term : {follow_term} - subject_id : {subject_id} - Report_id : {report_id} : {activities[0]}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting activities for follow_term : {follow_term} - subject_id : {subject_id} - Report_id : {report_id} : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching activities")


        # try except block for processing activities data
        try:

            activities = process_activities_for_subjects_view(activities)
            log_manager.log("info", "Activities dates processed")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in formatting dates : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching activities")


        # try except block for processing subjects data
        try:
            for act in activities:
                act['json_subject_data'] = literal_eval( json.loads (act['json_subject_data']) )
                
            log_manager.log("info", "json_subject_data formatted")            

            grouped_activities = defaultdict(lambda: defaultdict(list))

            for activity in activities:
                subject_id = activity['subject_id']
                subject_data = activity['json_subject_data']                
                code_name = subject_data['CdCode']

                grouped_activities[subject_id][code_name].append(activity)

            for subject_id, subject_data in grouped_activities.items():

                for code_name, code_activities in subject_data.items():
                    formatted_activities={'code_name': code_name, 'activities': code_activities}
            
            log_manager.log("info", "Activities json data processed according to subjects, strands, sub-strands, and codes")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in formatting json data for activities for follow_term : {follow_term} - subject_id : {subject_id} - Report_id : {report_id} : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching activities")


        # try except to get count of activities for report
        try:

            count_query = """
                SELECT COUNT(*) AS total_records
                FROM 
                    activites
            """
            
            if follow_term == 1:
                count_query += """
                JOIN 
                    states_has_terms ON activites.states_has_terms_id = states_has_terms.id
                """

            if where_conditions:
                count_query += " WHERE " + " AND ".join(where_conditions)
            
            self.cursor.execute(count_query, val[:-2])
            total_records = self.cursor.fetchone()["total_records"]
            pages = math.ceil(total_records / page_size)
            
            log_manager.log("info", f"Successfully fetched {total_records} activities for follow_term : {follow_term} - subject_id : {subject_id} - Report_id : {report_id}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting count of activities for follow_term : {follow_term} - subject_id : {subject_id} - Report_id : {report_id} : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in fetching activities")


        return jsonify(
            {
                "status": 200,
                "message": "Request was successful",
                "data": formatted_activities,
                "total_records": total_records,
                "pages": pages,
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def put(self):
        """Get S3 urls for files"""
        log_manager.log("success", "=== PUT generate S3 post urls API ===")

        # try except block for API body parameters
        try:
            self.files_args.remove_argument("report_id")
            self.files_args.remove_argument("description")
            self.files_args.remove_argument("file_ids")

            args = self.files_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in generating S3 post urls")

        try:
            file_urls = generate_aws_signature_v4_post_urls(args["file_names"])
            log_manager.log("info", f"Links generated for posting file to S3.")
            return jsonify(urls=file_urls)

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error generating S3 upload urls : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in S3 post urls")


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """Add Activity Route"""
        log_manager.log("success", "=== POST add activity API ===")

        # try except block for API body parameters
        try:
            args = self.activity_args.parse_args()
            
        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding activity")


        # try except block for checking report id
        try:
            report_id = args["report_id"]

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing report_id for add activity : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding Activity")


        # try except block for getting existing date ranges
        try:
            """initially we got all the date ranges existing for that report id"""
            date_ranges_query = """
                    SELECT
                        act_start_date AS start_date,
                        act_end_date AS end_date
                    FROM activites
                    WHERE 
                        report_id = %s
                        AND act_start_date IS NOT NULL 
                        AND act_end_date IS NOT NULL
                    GROUP BY act_start_date , act_end_date
                    ORDER BY act_start_date DESC
                    """

            self.cursor.execute(date_ranges_query, (report_id,))
            date_ranges = self.cursor.fetchall()

            log_manager.log("info", f"Date ranges for report id : {report_id} in add activity - data : {date_ranges}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error fetching date ranges for report_id : {report_id}: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding Activity")


        if not args["end_date"]:
            single_date_activity = datetime.strptime(args["start_date"], "%Y-%m-%d").date()
            args["single_date_activity"] = single_date_activity

            for d_range in date_ranges:
                if d_range["start_date"] <= single_date_activity <= d_range["end_date"]:
                    args["start_date"] = d_range["start_date"]
                    args["end_date"] = d_range["end_date"]
        else:
            args["single_date_activity"] = None
            
        current_date = date.today()


        # try except block for inserting activity
        try:
            self.cursor.execute(
                """ INSERT INTO activites 
                    (act_start_date,act_end_date,description,attached_links,created_date,inserted_date,
                    last_updated_date,json_subject_data,report_id,states_has_terms_id,subject_id) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        args["start_date"],
                        args["end_date"],
                        args["description"],
                        args["urls"],
                        args["single_date_activity"],
                        current_date,
                        current_date,
                        json.dumps(args["json_data"]),
                        args["report_id"],
                        args["states_has_terms_id"],
                        args["subject_id"]
                    ),
            )
            self.db.commit()
            last_entered_activity = self.cursor.lastrowid
            log_manager.log("info", f"Activity added in DB with id : {last_entered_activity} - data : {args}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error adding activity to DB : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding Activity")


        if args["file_names"] != "--list":
            for i in range(len(args["file_names"])):
                
                # try except block for entering new files for activity
                try:

                    self.cursor.execute(
                        """INSERT INTO activity_files 
                        (file_name, added_date, isDeleted, activites_id) 
                        VALUES (%s, %s, %s, %s)""",
                        (args["file_names"][i], current_date, 0, last_entered_activity),
                    )
                    self.db.commit()
                    last_entered_activity_file = self.cursor.lastrowid
                    activity_files_data = {
                        "id" : last_entered_activity_file,
                        "file_name" : args["file_names"][i],
                        "added_date" : current_date,
                        "isDeleted" : 0
                    }
                    log_manager.log("info", f"New file entered for activity id : {last_entered_activity} - data : {activity_files_data}")

                except Exception as e:
                    capture_exception(e)
                    log_manager.log("error", f"Error inserting new files for activity : {e}")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    abort(http_status_code=501, message="Error in adding Activity")


        # try except block for updating report for current activity
        try:
            self.cursor.execute(
                """ UPDATE report
                    SET last_edited = %s
                    WHERE id = %s 
                """,
                (
                    current_date,
                    args["report_id"],
                ),
            )
            self.db.commit()
            log_manager.log("info", f"Report id : {args['report_id']} updated for activity.")
        
        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error updating report while adding activity  - {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in adding Activity")
        
        log_manager.log("info", f"Activity added with id : {last_entered_activity}")
        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify({"status": 200, "message": "Activity added Successful"})


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def patch(self):
        """Edit activity Routes"""
        log_manager.log("success", "=== Patch edit activity API ===")

        # try except block for API body parameters
        try:
            add_args = self.files_args.parse_args()

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing activity")

        current_date = date.today()

        # try except block for checking activity id
        try:
            activity_id = int(request.args.get("activity_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing activity_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing activity")


        # try except block for editing activity description
        try:
            self.cursor.execute(
                """
                    UPDATE activites 
                    SET 
                        description=%s,
                        attached_links=%s,
                        last_updated_date=%s,
                        json_subject_data=%s,
                        subject_id=%s
                    WHERE 
                        id=%s""",
                (
                    add_args["description"],
                    add_args["urls"],
                    current_date,
                    json.dumps(add_args["json_data"]),
                    add_args["subject_id"],
                    activity_id
                ),
            )
            self.db.commit()
            log_manager.log("info", f"Data edited for activity id : {activity_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error updating activity data : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing activity")


        if add_args["file_ids"] != "--list":
            for i in range(len(add_args["file_ids"])):

                # try except block for updating activity files status to 0
                try:
                    self.cursor.execute(
                        "UPDATE activity_files set isDeleted=1 where id=%s and activites_id = %s",
                        (add_args["file_ids"][i], activity_id),
                    )
                    self.db.commit()
                    log_manager.log("info", f"Updated status for file_id : {add_args['file_ids'][i]} for activity id : {activity_id}")

                except Exception as e:
                    capture_exception(e)
                    log_manager.log("error", f"Error updating activity files status : {e}")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    abort(http_status_code=501, message="Error in editing activity")


        if add_args["file_names"] != "--list":
            for i in range(len(add_args["file_names"])):

                # try except block for entering new files for activity
                try:
                    self.cursor.execute(
                        """INSERT INTO activity_files 
                        (file_name, added_date, isDeleted, activites_id) 
                        VALUES (%s, %s, %s, %s)""",
                        (add_args["file_names"][i], current_date, 0, activity_id),
                    )
                    self.db.commit()
                    last_entered_activity_file = self.cursor.lastrowid
                    activity_files_data = {
                        "id" : last_entered_activity_file,
                        "file_name" : add_args["file_names"][i],
                        "added_date" : current_date,
                        "isDeleted" : 0,
                        "activites_id" : activity_id
                    }
                    log_manager.log("info", f"New file entered for activity id : {activity_id} - data : {activity_files_data}")

                except Exception as e:
                    capture_exception(e)
                    log_manager.log("error", f"Error inserting new files for activity : {e}")
                    MySqlDatabase.close_connection(self.cursor, self.db)
                    log_manager.log("info", "======================")
                    abort(http_status_code=501, message="Error in editing activity")


        # try except block for updating report for current activity
        try:
            self.cursor.execute(
                """ UPDATE report
                    SET last_edited = %s
                    WHERE id = %s 
                """,
                (
                    current_date,
                    add_args["report_id"],
                ),
            )
            self.db.commit()
            log_manager.log("info", f"Report id : {add_args['report_id']} updated for activity id : {activity_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error updating report while editing activity id :{activity_id} - {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in editing activity")


        log_manager.log("info", f"Activity edited with id : {activity_id}")
        MySqlDatabase.close_connection(self.cursor, self.db)
        log_manager.log("info", "======================")
        return jsonify({"status": 200, "message": "Activity Edited Successfully"})


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def delete(self):
        """Delete Activity"""
        log_manager.log("success", "=== DELETE activity API ===")

        # try except block for checking activity id
        try:
            activity_id = int(request.args.get("activity_id"))

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing activity_id: {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting activity")

        # try except block for deleting activity query
        try:
            query = """delete from activites where id=%s"""
            self.cursor.execute(query, (activity_id,))
            self.db.commit()

            log_manager.log("info", f"Activity deleted with id : {activity_id}")

            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            return jsonify({"status": 200, "message": "Activity Deleted Successfully"})

        except Exception as e:
            capture_exception(e)
            error_message = f"Error deleting Activity : {e}"
            log_manager.log("error", error_message)
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in deleting Activity")
