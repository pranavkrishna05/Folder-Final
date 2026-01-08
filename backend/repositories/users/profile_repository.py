import sqlite3
from datetime import datetime
from typing import Optional
from backend.models.users.profile import Profile
import logging

logger = logging.getLogger(__name__)

class ProfileRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def get_profile_by_user_id(self, user_id: int) -> Optional[Profile]:
        logger.info("Fetching profile for user_id=%s", user_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, first_name, last_name, phone_number, address, preferences, created_at, updated_at FROM profiles WHERE user_id=?",
                (user_id,),
            )
            row = cursor.fetchone()
            return Profile(*row) if row else None

    def update_profile(self, user_id: int, first_name: str, last_name: str, phone_number: str | None, address: str | None, preferences: str | None) -> Profile:
        logger.info("Updating profile for user_id=%s", user_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE profiles
                SET first_name=?, last_name=?, phone_number=?, address=?, preferences=?, updated_at=?
                WHERE user_id=?
                """,
                (first_name, last_name, phone_number, address, preferences, datetime.now(), user_id),
            )
            conn.commit()
            return self.get_profile_by_user_id(user_id)

    def create_profile(self, user_id: int, first_name: str, last_name: str, phone_number: str | None = None, address: str | None = None, preferences: str | None = None) -> Profile:
        logger.info("Creating profile for user_id=%s", user_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.now()
            cursor.execute(
                """
                INSERT INTO profiles (user_id, first_name, last_name, phone_number, address, preferences, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, first_name, last_name, phone_number, address, preferences, created_at, created_at),
            )
            profile_id = cursor.lastrowid
        return Profile(id=profile_id, user_id=user_id, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, preferences=preferences, created_at=created_at, updated_at=created_at)