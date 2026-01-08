import sqlite3
import secrets
from datetime import datetime, timedelta
from backend.models.users.password_reset_token import PasswordResetToken
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class PasswordResetRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def create_reset_token(self, user_id: int) -> PasswordResetToken:
        token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(hours=24)
        logger.info("Creating password reset token for user_id=%s", user_id)
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO password_reset_tokens (user_id, token, expires_at, used, created_at) VALUES (?, ?, ?, 0, ?)",
                (user_id, token, expires_at, datetime.now()),
            )
            token_id = cur.lastrowid
        return PasswordResetToken(
            id=token_id, user_id=user_id, token=token, expires_at=expires_at, used=False, created_at=datetime.now()
        )

    def get_valid_token(self, token: str) -> Optional[PasswordResetToken]:
        logger.info("Fetching valid password reset token")
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, user_id, token, expires_at, used, created_at FROM password_reset_tokens WHERE token=? AND used=0 AND expires_at > ?",
                (token, datetime.now()),
            )
            row = cur.fetchone()
            return PasswordResetToken(*row) if row else None

    def mark_token_as_used(self, token: str) -> None:
        logger.info("Marking token as used")
        with self._get_connection() as conn:
            conn.execute("UPDATE password_reset_tokens SET used=1 WHERE token=?", (token,))