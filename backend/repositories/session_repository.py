import sqlite3
import logging
from datetime import datetime
from models.session import Session

logger = logging.getLogger(__name__)

class SessionRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def create_session(self, user_id: int, token: str, expires_at: datetime) -> Session:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)",
            (user_id, token, expires_at),
        )
        connection.commit()
        session_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, user_id, token, created_at, expires_at FROM sessions WHERE id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            raise ValueError("Failed to create session.")
        return Session(*row)