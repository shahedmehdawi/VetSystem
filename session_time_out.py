import mysql.connector

class Session:
    def __init__(self):
        self.time_duration = 120    
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bella*8234",
            database="new_schema"
        )
        self.start_time = self.read_from_db()

    def read_from_db(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT NOW()")
        current_time = cursor.fetchone()[0]
        return current_time

    def has_timed_out(self):
        current_time = self.read_from_db()
        time_difference = (current_time - self.start_time).total_seconds()
        return time_difference >= self.time_duration