import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')

class ElaborationData:

    def __init__(self):
        self.original_elaborations = []
        self.vectorizer = None
        self.processed_elaborations = []

    @staticmethod
    def tokenize(text):
        tokens = word_tokenize(text)
        return tokens

    @staticmethod
    def remove_stopwords(tokens):
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        return filtered_tokens

    def preprocess(self, text):
        if text is None:
            return ""
        text = text.lower()
        tokens = self.tokenize(text)
        filtered_tokens = self.remove_stopwords(tokens)
        return ' '.join(filtered_tokens)

    def get_distinct_level_ids(self, MySqlDatabase, user_id, log_manager):
        cursor, db = MySqlDatabase.connection()

        query_levels = "SELECT DISTINCT level_id FROM child WHERE user_id = %s"
        cursor.execute(query_levels, (user_id,))
        level_ids = [row['level_id'] for row in cursor.fetchall()]

        log_manager.log("success", f"Distinct level_ids for user {user_id}: {level_ids}")

        MySqlDatabase.close_connection(cursor, db)
        return level_ids

    def process_elaborations(self, level_id, rows, log_manager):
        elaborations = [row['elaboration'] for row in rows if row['elaboration'] is not None]

        log_manager.log("success", f"Total elaborations for level id {level_id}: {len(elaborations)} ")

        self.original_elaborations = elaborations

        elaborations = [text.replace('\n', ' ').replace('\r', '') for text in elaborations]

        elaborations_processed = [self.preprocess(text) for text in elaborations]
        self.processed_elaborations = elaborations_processed

        log_manager.log("info", "Elaborations processed")

    def get_elaborations_from_db(self, MySqlDatabase, level_id, log_manager):
        cursor, db = MySqlDatabase.connection()

        query_elaborations = """
            SELECT JSON_UNQUOTE(JSON_EXTRACT(subject_data.json_data, '$.Elaboration')) as elaboration
            FROM subject_data
            JOIN subject ON subject_data.subject_id = subject.id
            JOIN learning ON subject.learning_id = learning.id
            JOIN level ON learning.level_id = level.id
            WHERE level.id = %s
            AND JSON_UNQUOTE(JSON_EXTRACT(subject_data.json_data, '$.Elaboration')) IS NOT NULL
            AND JSON_UNQUOTE(JSON_EXTRACT(subject_data.json_data, '$.Elaboration')) != 'null'
        """
        cursor.execute(query_elaborations, (level_id,))
        rows = cursor.fetchall()

        self.process_elaborations(level_id, rows, log_manager)

        MySqlDatabase.close_connection(cursor, db)
