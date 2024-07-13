"""Modules"""
import json
import numpy as np
from flask import jsonify
from flask_restful import Resource, reqparse, request, abort
from sklearn.feature_extraction.text import TfidfVectorizer
from config import MySqlDatabase, log_manager, cache, AI_object
from sklearn.metrics.pairwise import cosine_similarity
from sentry_sdk import capture_exception
from utils import (
    jwt_required,
    role
)
from flask_jwt_extended import get_jwt_identity

# ROUTES DEFINITIONS
class AIActivity(Resource):
    """Activity Routes"""

    def __init__(self):
        # db connection
        self.cursor, self.db = MySqlDatabase.connection()

        self.AI_activity_args = reqparse.RequestParser()
        self.AI_activity_args.add_argument(
            "level_id", type=int, help="level id of child", required=True
        )
        self.AI_activity_args.add_argument(
            "description", type=str, help="activity description", required=True
        )


        self.AI_data_fetch_args = reqparse.RequestParser()
        self.AI_data_fetch_args.add_argument(
            "elaboration", type=str, help="selected elaboration", required=True
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def post(self):
        """Match elaborations route"""
        log_manager.log("success", "=== POST Match elaborations API ===")

        # try except block for API body parameters
        try:
            args = self.AI_activity_args.parse_args()
            level_id = str(args['level_id'])
            user_id = get_jwt_identity()
            user_id_str = str(user_id)

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting matched elaborations")


        cache_data = cache.get('users_data')
        # log_manager.log("info", f"cache_data : {cache_data}")
        # try except block for for getting elaborations from cache
        try:
            
            user_data = cache_data.get(user_id_str)
            if user_data is None:
                raise ValueError(f"No data in cache for user_id_str : {user_id_str}")
            
            level_data = user_data.get(level_id)
            if level_data is None:
                raise ValueError(f"No data in cache for level_id : {level_id}")
            
            original_elaborations = level_data.get('original_elaborations')
            processed_elaborations = level_data.get('processed_elaborations')

            log_manager.log("info", f"Original elaborations for level {level_id}: {len(original_elaborations)}")
            log_manager.log("info", f"Processed elaborations for level {level_id}: {len(processed_elaborations)}")

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting data from cache : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting matched elaborations")


        # try except block for for getting elaborations from redis
        try:
            user_input_processed = AI_object.preprocess(args['description'])
            vectorizer = TfidfVectorizer()
            all_texts = [user_input_processed] + processed_elaborations
            tfidf_matrix = vectorizer.fit_transform(all_texts)
    
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            top_indices = np.argsort(similarity_matrix[0])[-3:][::-1]
            
            top_elaborations_with_scores = [(original_elaborations[index], similarity_matrix[0][index]) for index in top_indices]

            matched_elaborations = []

            if all(score == 0 for _, score in top_elaborations_with_scores):
                message = "No elaborations matched. Try again"
                log_manager.log("warning", f"{message}")
                MySqlDatabase.close_connection(self.cursor, self.db)
                log_manager.log("info", "======================")
                response = jsonify(status=501, message=message)
                response.status_code = 501
                return response
            else:
                for rank, (top_elaboration, similarity_score) in enumerate(top_elaborations_with_scores, start=1):
                    matched_elaborations.append(top_elaboration)

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting matches using cosine : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting matched elaborations")

        return jsonify(
            {
                "status": 200,
                "message": "Request was successful.",
                "data": matched_elaborations
            }
        )


    @role(refresh=False, user_role="User")
    @jwt_required(refresh=False)
    def patch(self):
        """Get matched elaboration data route"""
        log_manager.log("success", "=== PATCH Get matched elaboration data API ===")

        # try except block for API body parameters
        try:
            args = self.AI_data_fetch_args.parse_args()
            
        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error parsing body arguements : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting matched elaboration data")


        # try except block for for getting elaborations from redis
        try:
                query = """
                    SELECT 
                        subject_data.id,
                        subject_data.json_data, 
                        subject.name AS subject_name, 
                        learning.name AS learning_area,
                        subject_data.subject_id
                    FROM 
                        subject_data
                    JOIN 
                        subject ON subject_data.subject_id = subject.id
                    JOIN 
                        learning ON subject.learning_id = learning.id
                    WHERE 
                        JSON_UNQUOTE(JSON_EXTRACT(subject_data.json_data, '$.Elaboration')) = %s
                """
                self.cursor.execute(query, (args['elaboration'],))
                record = self.cursor.fetchone()
                
                data = json.loads(record['json_data'])
                for key,value in data.items():
                    record[key] = value

        except Exception as e:
            capture_exception(e)
            log_manager.log("error", f"Error getting matches using cosine : {e}")
            MySqlDatabase.close_connection(self.cursor, self.db)
            log_manager.log("info", "======================")
            abort(http_status_code=501, message="Error in getting matched elaborations")

        return jsonify(
            {
                "status": 200,
                "message": "Request was successful.",
                "data": record
            }
        )
