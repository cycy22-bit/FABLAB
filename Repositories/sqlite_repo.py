import sqlite3
from sqlite3 import Row


class SQLiteRepository:

    def __init__(self, database_path: str):
        self.database_path = database_path

    def get_connection(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = Row
        return conn

    def fetch_all(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def fetch_one(self, query: str, params: tuple = ()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return row

    def execute(self, query: str, params: tuple = ()) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True