import sqlite3
import logging
from models.user import User
from typing import Optional

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def create_user(self, email: str, password_hash: str) -> User:
        logger.info("Inserting new user into the database")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash),
        )
        connection.commit()
        user_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, email, password_hash, created_at, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            raise ValueError("Failed to retrieve created user.")
        return User(
            id=row[0],
            email=row[1],
            password_hash=row[2],
            created_at=row[3],
            updated_at=row[4],
        )

    def find_by_email(self, email: str) -> Optional[User]:
        logger.info(f"Searching for user by email: {email}")
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
        return User(
            id=row[0],
            email=row[1],
            password_hash=row[2],
            created_at=row[3],
            updated_at=row[4],
        )