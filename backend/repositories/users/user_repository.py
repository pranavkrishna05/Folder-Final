from typing import Optional, List
import sqlite3
from backend.models.users.user import User
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def create_user(self, email: str, password_hash: str) -> User:
        logger.info("Creating user with email=%s", email)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now()
            cursor.execute(
                "INSERT INTO users (email, password_hash, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (email, password_hash, now, now),
            )
            user_id = cursor.lastrowid
            return User(id=user_id, email=email, password_hash=password_hash, created_at=now, updated_at=now)

    def get_user_by_email(self, email: str) -> Optional[User]:
        logger.info("Fetching user by email=%s", email)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, created_at, updated_at FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return User(*row)
            return None

    def list_users(self) -> List[User]:
        logger.info("Listing all users")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, created_at, updated_at FROM users")
            rows = cursor.fetchall()
            return [User(*row) for row in rows]