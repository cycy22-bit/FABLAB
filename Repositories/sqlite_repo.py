import sqlite3
from pathlib import Path
from typing import Any


class SQLiteRepository:
    """
    Classe mère de tous les repositories SQLite.
    Elle gère uniquement la connexion à la base de données.
    """

    def __init__(self, db_path: str = "Database/fablab.db"):
        self.db_path = db_path
        self._ensure_database_file()

    def _ensure_database_file(self) -> None:
        path = Path(self.db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute(query, params)
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur SQLite execute : {e}")
            return False

    def execute_insert(self, query: str, params: tuple[Any, ...] = ()) -> int | None:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur SQLite execute_insert : {e}")
            return None

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite fetch_all : {e}")
            return []

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur SQLite fetch_one : {e}")
            return None