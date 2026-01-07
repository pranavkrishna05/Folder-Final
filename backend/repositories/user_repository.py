import sqlite3
from typing import Optional
import logging
from models.user import User

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_by_email(self, email: str) -> Optional[User]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, email, password_hash, created_at, updated_at FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return User(*row)

    def update_password(self, user_id: int, password_hash: str) -> None:
        logger.info(f"Updating password for user id {user_id}")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (password_hash, user_id),
        )
        connection.commit()
        connection.close()