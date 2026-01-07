import sqlite3
import logging
from typing import Optional
from models.user import User

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_by_email(self, email: str) -> Optional[User]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, email, password_hash, failed_attempts, is_locked, last_login_at, created_at, updated_at FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return User(*row)

    def update_failed_attempts(self, email: str, attempts: int, lock: bool) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET failed_attempts = ?, is_locked = ? WHERE email = ?",
            (attempts, int(lock), email),
        )
        connection.commit()
        connection.close()

    def update_last_login(self, user_id: int) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET last_login_at = CURRENT_TIMESTAMP, failed_attempts = 0 WHERE id = ?",
            (user_id,),
        )
        connection.commit()
        connection.close()