import sqlite3
from typing import Optional
from datetime import datetime
from backend.models.users.user import User
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def get_user_by_email(self, email: str) -> Optional[User]:
        logger.info("Fetching user by email=%s", email)
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, email, password_hash, failed_login_attempts, is_locked, last_login_at, created_at, updated_at FROM users WHERE email=?",
                (email,),
            )
            row = cur.fetchone()
            return User(*row) if row else None

    def update_login_attempts(self, user_id: int, failed_login_attempts: int, is_locked: bool) -> None:
        logger.info("Updating login attempts for user_id=%s", user_id)
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET failed_login_attempts=?, is_locked=?, updated_at=? WHERE id=?",
                (failed_login_attempts, is_locked, datetime.now(), user_id),
            )

    def update_last_login(self, user_id: int) -> None:
        logger.info("Updating last login for user_id=%s", user_id)
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET last_login_at=?, updated_at=? WHERE id=?",
                (datetime.now(), datetime.now(), user_id),
            )