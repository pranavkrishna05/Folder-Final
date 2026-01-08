import logging
from backend.repositories.users.user_repository import UserRepository
from backend.services.auth.password_utils import hash_password
from backend.models.users.user import User

logger = logging.getLogger(__name__)

class RegistrationService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def register_user(self, email: str, password: str) -> User:
        existing_user = self._user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        password_hash = hash_password(password)
        return self._user_repository.create_user(email, password_hash)