import sqlite3
import logging
from typing import Optional
from models.password_reset import PasswordReset

logger = logging.getLogger(__name__)

class PasswordResetRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def create_token(self, user_id: int, token: str, expires_at: str) -> PasswordReset:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO password_resets (user_id, token, expires_at) VALUES (?, ?, ?)",
            (user_id, token, expires_at),
        )
        connection.commit()
        reset_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, user_id, token, expires_at, created_at, used FROM password_resets WHERE id = ?",
            (reset_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            raise ValueError("Failed to create password reset token.")
        return PasswordReset(*row)

    def find_by_token(self, token: str) -> Optional[PasswordReset]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, user_id, token, expires_at, created_at, used FROM password_resets WHERE token = ?",
            (token,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return PasswordReset(*row)

    def mark_used(self, token: str) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE password_resets SET used = 1 WHERE token = ?",
            (token,),
        )
        connection.commit()
        connection.close()