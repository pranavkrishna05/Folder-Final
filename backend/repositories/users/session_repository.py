import sqlite3
from datetime import datetime, timedelta
import secrets
from typing import Optional
from backend.models.users.session import Session
import logging

logger = logging.getLogger(__name__)

class SessionRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def create_session(self, user_id: int, timeout_minutes: int = 30) -> Session:
        token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(minutes=timeout_minutes)
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO sessions (user_id, token, expires_at, created_at) VALUES (?, ?, ?, ?)",
                (user_id, token, expires_at, datetime.now()),
            )
            session_id = cur.lastrowid
        logger.info("Created new session for user_id=%s", user_id)
        return Session(id=session_id, user_id=user_id, token=token, expires_at=expires_at, created_at=datetime.now())

    def get_session_by_token(self, token: str) -> Optional[Session]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, user_id, token, expires_at, created_at FROM sessions WHERE token=?", (token,))
            row = cur.fetchone()
            return Session(*row) if row else None

    def delete_session(self, token: str) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        logger.info("Deleted session with token=%s", token)