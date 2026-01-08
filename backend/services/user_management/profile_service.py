import logging
from backend.repositories.users.profile_repository import ProfileRepository
from backend.models.users.profile import Profile

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self, profile_repository: ProfileRepository) -> None:
        self._profile_repository = profile_repository

    def get_user_profile(self, user_id: int) -> Profile:
        profile = self._profile_repository.get_profile_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found")
        return profile

    def update_user_profile(
        self, user_id: int, first_name: str, last_name: str, phone_number: str | None, address: str | None, preferences: str | None
    ) -> Profile:
        logger.info("Updating user profile for user_id=%s", user_id)
        return self._profile_repository.update_profile(user_id, first_name, last_name, phone_number, address, preferences)

    def create_profile_for_user(
        self, user_id: int, first_name: str, last_name: str, phone_number: str | None = None, address: str | None = None, preferences: str | None = None
    ) -> Profile:
        logger.info("Creating profile for user_id=%s", user_id)
        return self._profile_repository.create_profile(user_id, first_name, last_name, phone_number, address, preferences)