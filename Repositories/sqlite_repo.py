import sqlite3
import logging
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class RepositoryError(Exception):
    pass


class SQLiteRepository:
    TABLE: str = ""
    PK: str = ""
    DTO_CLASS = None

    def __init__(self, db_path: str = "Database/fablab.db"):
        self.db_path = Path(db_path)
        self._ensure_database_file()

    def _ensure_database_file(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.touch(exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _normalize_value(self, value: Any) -> Any:
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return value

    def _to_dict(self, dto: Any) -> dict[str, Any]:
        if is_dataclass(dto):
            data = asdict(dto)
        else:
            data = dto.__dict__.copy()

        return {key: self._normalize_value(value) for key, value in data.items()}

    def _to_dto(self, row: sqlite3.Row):
        if row is None:
            return None
        return self.DTO_CLASS(**dict(row))

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erreur SQLite fetch_all : {e}")
            return []

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erreur SQLite fetch_one : {e}")
            return None

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute(query, params)
                conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Erreur SQLite execute : {e}")
            return False

    def execute_insert(self, query: str, params: tuple[Any, ...] = ()) -> int | None:
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Erreur SQLite execute_insert : {e}")
            return None

    def get_all(self):
        rows = self.fetch_all(f"SELECT * FROM {self.TABLE}")
        return [self._to_dto(row) for row in rows]

    def get_by_id(self, id_value: int):
        row = self.fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE {self.PK} = ?",
            (id_value,),
        )
        return self._to_dto(row) if row else None

    def create(self, dto: Any) -> bool:
        data = self._to_dict(dto)
        data.pop(self.PK, None)

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))

        query = f"""
        INSERT INTO {self.TABLE} ({columns})
        VALUES ({placeholders})
        """

        return self.execute(query, tuple(data.values()))

    def update(self, dto: Any) -> bool:
        data = self._to_dict(dto)

        if self.PK not in data or data[self.PK] is None:
            logging.error(f"{self.PK} manquant pour update.")
            return False

        pk_value = data.pop(self.PK)
        assignments = ", ".join([f"{column}=?" for column in data.keys()])

        query = f"""
        UPDATE {self.TABLE}
        SET {assignments}
        WHERE {self.PK}=?
        """

        return self.execute(query, tuple(data.values()) + (pk_value,))

    def delete(self, id_value: int) -> bool:
        return self.execute(
            f"DELETE FROM {self.TABLE} WHERE {self.PK}=?",
            (id_value,),
        )