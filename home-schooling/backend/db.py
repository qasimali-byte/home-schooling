"""Modules"""
import mysql.connector
from sentry_sdk import capture_exception

# class to handle data base query and connect to the mysql
class DatabaseConnection:
    """Database connection class"""

    def __init__(self, host, databasename, charset, user, password, port , LogManager):
        self.host = host
        self.databasename = databasename
        self.charset = charset
        self.user = user
        self.password = password
        self.port = port
        self.log_manager = LogManager

    # function to get a fresh cursor and database object
    def connection(self):
        """connection open function"""
        try:

            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                charset=self.charset,
                database=self.databasename,
            )
            assert db.is_connected(), "Error Connection!"

            self.log_manager.log("info", "Connected to the database")
            cursor = db.cursor(buffered=True, dictionary=True)
            return cursor, db

        except mysql.connector.Error as e:
            self.log_manager.log("error", f"Error connecting to MySQL : {e}")
            return None, None


    def close_connection(self, cursor, db):
        """connection close function"""
        try:

            cursor.close()
            if db and db.is_connected():
                db.close()
                self.log_manager.log("info", "Connection closed")
            else:
                self.log_manager.log("warning", "No connection to close.")
        
        except Exception as e:
            capture_exception(e)
            self.log_manager.log("error", f"Error closing connection : {e}")

