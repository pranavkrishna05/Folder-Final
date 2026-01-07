import sqlite3
from typing import Optional
from models.user import User

class UserRepository:
    def __init__(self, db_path: str = "database/app.db"):
        self._db_path = db_path

    def find_by_id(self, user_id: int) -> Optional[User]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, email, password_hash, created_at, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return User(*row)