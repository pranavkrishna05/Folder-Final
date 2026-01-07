import logging
from typing import Any
from models.user import User
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_profile(self, user_id: int) -> User | None:
        logger.info(f"Fetching profile for user id {user_id}")
        return self._user_repository.find_by_id(user_id)

    def update_profile(self, user_id: int, data: dict[str, Any]) -> User:
        logger.info(f"Updating profile for user id {user_id}")
        full_name = data.get("full_name")
        preferences = data.get("preferences", "")
        if not full_name:
            raise ValueError("Full name is required for profile update.")
        user = self._user_repository.update_profile(user_id, full_name, preferences)
        if not user:
            raise ValueError("User not found or unable to update profile.")
        logger.info(f"Profile updated successfully for user id {user_id}")
        return user