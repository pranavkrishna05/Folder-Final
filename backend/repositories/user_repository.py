import sqlite3
import logging
from typing import Optional
from models.user import User

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_by_id(self, user_id: int) -> Optional[User]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, email, full_name, preferences, created_at, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return User(*row)

    def update_profile(self, user_id: int, full_name: str, preferences: str) -> Optional[User]:
        logger.info(f"Updating profile for user id {user_id}")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET full_name = ?, preferences = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (full_name, preferences, user_id),
        )
        connection.commit()
        cursor.execute(
            "SELECT id, email, full_name, preferences, created_at, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return User(*row)