"""Modules"""
from ast import literal_eval
from collections import defaultdict
from datetime import date, datetime
import json
import os
from flask import jsonify
from flask_restful import Resource, reqparse, request, abort
from sentry_sdk import capture_exception
from config import MySqlDatabase,log_manager
from utils import (
    generate_download_url,
    jwt_required,
    process_file_array,
    role,
    PDF,
    process_pdf_content,
    process_pdf_header,
    upload_file_to_s3,
)


class DownloadActivity(Resource):
    """Download Activity Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        # Request arguments
        self.activity_args = reqparse.RequestParser()


    def make_query(self,follow_term):
        query = """
            SELECT
                activites.act_start_date,
                activites.act_end_date,
                activites.description AS activity_description,
                activites.attached_links,
                subject.id AS subject_id,
                subject.name AS subject_name,
                activites.json_subject_data,
                concat('[',
                        GROUP_CONCAT(JSON_OBJECT('id', activity_files.id, 'file_name', activity_files.file_name)
                                ),']') as file_array,
                report.name AS report_name,
                CONCAT(child.first_name, ' ', child.last_name) AS child_name,
                states.name AS state_name,
                level.name AS school_year,
                user.email,
                user.address
        """

        if follow_term == 1:
            query += """
                ,states_has_terms.terms_id AS state_terms_id"""

        query += """
            FROM 
                activites
            INNER JOIN 
                report ON activites.report_id = report.id
            INNER JOIN 
                child ON report.child_id = child.id
            INNER JOIN 
                user ON child.user_id = user.id
            INNER JOIN 
                states ON child.states_id = states.id
            INNER JOIN 
                level ON child.level_id = level.id
            LEFT JOIN 
                activity_files ON activites.id = activity_files.activites_id AND activity_files.isDeleted = 0
            INNER JOIN 
                subject ON activites.subject_id = subject.id
        """

        if follow_term == 1:
            query += """    INNER JOIN states_has_terms ON activites.states_has_terms_id = states_has_terms.id"""

        query += """
            WHERE 
                activites.report_id = %s
                AND subject.name = %s
                AND SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'CdCode': '", -1), "',", 1) = %s
                AND SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Strand': '", -1), "',", 1) = %s
                AND SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Substrand': '", -1), "',", 1) = %s
            GROUP BY 
                activites.id
            ORDER BY 
                subject.id DESC, activites.id DESC;       
        """

        return query

    def process_activities_data(self,activities):

        for activity in activities:
            start_date = activity.get("act_start_date")
            end_date = activity.get("act_end_date")

            if isinstance(start_date, date):
                formatted_start_date = start_date.strftime("%d %B %Y")
            else:
                formatted_start_date = start_date

            if end_date:
                if isinstance(end_date, date):
                    formatted_end_date = end_date.strftime("%d %B %Y")
                else:
                    formatted_end_date = end_date
            else:
                formatted_end_date = None

            file_array_str = activity["file_array"]
            (
                attached_files_ids,
                attached_files_names,
                attached_files_urls,
            ) = process_file_array(file_array_str)

            activity["attached_files_ids"] = attached_files_ids
            activity["attached_files_names"] = attached_files_names
            activity["attached_files_urls"] = attached_files_urls
            activity["act_start_date"] = formatted_start_date
            activity["act_end_date"] = formatted_end_date
            activity['json_subject_data'] = literal_eval( json.loads (activity['json_subject_data']) )
            activity.pop("file_array")


        return activities

    
    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def get(self):
        """download activities pdf route"""
        log_manager.log("success", "=== GET Download Activities PDF API ===")

        # try except block for checking API search query params
        try:
            report_id, follow_term = (
                int(request.args.get("report_id")),
                int(request.args.get("follow_term")),
            )

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing query params : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading report")


        if follow_term not in [0, 1]:
            message = f"Wrong parameter given for follow_term "
            log_manager.log("error", message + f": {follow_term}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message=message)


        # try except block for getting groups of subject>code>strand>substrand
        try:
            query_subject = """
                SELECT
                    CAST(subject.name AS CHAR) AS name,
                    CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'CdCode': '", -1), "',", 1) AS CHAR) AS CdCode,
                    CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Strand': '", -1), "',", 1) AS CHAR) AS strand_name,
                    CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(json_subject_data, "'Substrand': '", -1), "',", 1) AS CHAR) AS sub_strand_name
                FROM 
                    activites JOIN subject ON activites.subject_id = subject.id
                WHERE
                    report_id = %s
                GROUP BY
                    subject_id, CdCode, strand_name, sub_strand_name

            """
            self.cursor.execute(query_subject, (report_id,))
            subject_data_rows = self.cursor.fetchall()

            if not subject_data_rows:
                log_manager.log("info", f"Successfully fetched. No subject groups for follow_term : {follow_term} - Report_id : {report_id}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")

                return jsonify(
                    {
                        "status": 200,
                        "message": "Request was successful. No subjects group found for this report.",
                        "data": [],
                    }
                )

            log_manager.log("info", f"Successfully fetched {len(subject_data_rows)} groups for follow_term : {follow_term} - Report_id : {report_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error fetching subject groups : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")


        # try except block for making generic json dict
        try:
            grouped_subjects = defaultdict(lambda: defaultdict(list))
            for row in subject_data_rows:
                subject_name = str(row['name'])
                code_name = str(row['CdCode'])
                strand_name = str(row['strand_name'])
                sub_strand_name = str(row['sub_strand_name'])
                
                grouped_subjects[subject_name][(code_name, strand_name, sub_strand_name)].append(row)

            log_manager.log("info", "Made generic dictionary to store data")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error making generic dictionary : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")


        # try except block for getting data for each group
        try:
            formatted_activities = []

            for subject_name, code_strand_sub_strand_groups in grouped_subjects.items():
                subject_activities = {'subject_name': subject_name, 'groups': []}

                for (code_name, strand_name, sub_strand_name), rows in code_strand_sub_strand_groups.items():
                    
                    # try except block getting activities data for group
                    try:
                        query = self.make_query(follow_term)
                        val = (report_id, subject_name, code_name, strand_name, sub_strand_name)
                        self.cursor.execute(query, val)
                        activities = self.cursor.fetchall()
                        log_manager.log("info", f"Fetched {len(activities)} activities for group")

                    except Exception as e:
                        capture_exception(e)
                        log_manager.log("error", f"Error fetching activities data : {e}")
                        abort(http_status_code=501, message="Error in downloading PDF")


                    # try except block for date formatting, processing files and json data
                    try:
                        processed_activities = self.process_activities_data(activities)
                        log_manager.log("info", "Date formatted, processed files and json data")

                    except Exception as e:
                        capture_exception(e)
                        log_manager.log("error", f"Error processing activities data : {e}")
                        abort(http_status_code=501, message="Error in downloading PDF")


                    group_activities = {
                        'CdCode': code_name,
                        'Strand': strand_name,
                        'Substrand': sub_strand_name,
                        'activities': processed_activities
                    }
                    subject_activities['groups'].append(group_activities)

                formatted_activities.append(subject_activities)

            log_manager.log("info", "Groups data fetched and formatted")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting groups data : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")


        first_activity = formatted_activities[0]['groups'][0]['activities'][0]

        report_pdf = "PDF"
        current_time = datetime.now()
        timestamp_formatted = current_time.strftime("%d%m%Y_%H%M%S")

        if follow_term == 1:
            report_pdf += f"_term_{timestamp_formatted}.pdf"
        
        elif follow_term == 0:
            report_pdf += f"_non_term_{timestamp_formatted}.pdf"

        pdf = PDF()
        pdf.add_page(orientation="P")


        # try except block for generating header of the pdf
        try:
            
            process_pdf_header(pdf, first_activity)
            log_manager.log("info", f"Successfully made PDF header for follow_term : {follow_term} - Report_id : {report_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error making PDF header for follow_term : {follow_term} - Report_id : {report_id} : {e}")
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")


        total_items = len(formatted_activities)

        for subject_data in formatted_activities:

            pdf.subject_heading = subject_data['subject_name']

            # try except block for making subject heading
            try:
                pdf.write_subject_heading()
                log_manager.log("info", f"Successfully made PDF heading for follow_term : {follow_term} - Report_id : {report_id}")

            except Exception as e:
                capture_exception(e)
                log_manager.log("error", f"Error in making PDF heading for follow_term : {follow_term} - Report_id : {report_id} : {e}")
                log_manager.log("info", "======================")
                abort(http_status_code=501, message="Error in downloading PDF")
            
            groups_data = subject_data['groups']
            for group in groups_data:

                pdf.strand_subheading = group['Strand']
                pdf.substrand_subheading = group['Substrand']
                pdf.code_subheading = group['CdCode']
                pdf.code_desc_subheading = group['activities'][0]['json_subject_data'].get('ContentDesc')

                # try except block for making strand,substrand,code subheading
                try:
                    pdf.write_subheading()

                except Exception as e:
                    capture_exception(e)
                    log_manager.log("error", f"Error in making PDF subheading for follow_term : {follow_term} - Report_id : {report_id} : {e}")
                    log_manager.log("info", "======================")
                    abort(http_status_code=501, message="Error in downloading PDF")


                code_activities = group['activities']
                # try except block for writing activity content in PDF
                try:
                    if follow_term == 1:
                        process_pdf_content(pdf, code_activities , True)
                    elif follow_term == 0:
                        process_pdf_content(pdf, code_activities , False)

                except Exception as e:
                    capture_exception(e)
                    log_manager.log("error", f"Error in making PDF activity details for follow_term : {follow_term} - Report_id : {report_id} : {e}")
                    log_manager.log("info", "======================")
                    abort(http_status_code=501, message="Error in downloading PDF")

        log_manager.log("info", f"Successfully added PDF content for follow_term : {follow_term} - Report_id : {report_id}")
            

        # try except block for final PDF generation
        try:
            pdf.output(report_pdf)
            log_manager.log("info", f"Successfully made PDF file for follow_term : {follow_term} - Report_id : {report_id}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error in PDF file creation for follow_term : {follow_term} - Report_id : {report_id} : {e}")
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")


        # try except block for uploading file to s3
        try:
            upload_file_to_s3(report_pdf)
            log_manager.log("info", f"Successfully uploaded PDF file to S3 for follow_term : {follow_term} - Report_id : {report_id}")

        except Exception as e:
            os.remove(report_pdf)
            capture_exception(e)
            message = "Error uploading file."
            log_manager.log("error", f"Error uploading file for follow_term : {follow_term} - Report_id : {report_id} : {e}")
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")


        # try except block for generating download file link
        try:
            download_url = generate_download_url(report_pdf)
            log_manager.log("info", f"Successfully generated PDF download link for follow_term : {follow_term} - Report_id : {report_id}")
            log_manager.log("info", "======================")
            os.remove(report_pdf)
            return jsonify(report_url=download_url)

        except Exception as e:
            os.remove(report_pdf)
            capture_exception(e)
            message = f"Error generating pre-signed URL for file"
            log_manager.log("error", f"Error generating pre-signed URL for file for follow_term : {follow_term} - Report_id : {report_id} : {e}")
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in downloading PDF")
