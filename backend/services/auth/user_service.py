import hashlib
import logging
from repositories.user_repository import UserRepository
from models.user import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def register_user(self, email: str, password: str) -> User:
        logger.info("Starting user registration process")
        existing = self._user_repository.find_by_email(email)
        if existing:
            raise ValueError("Email already registered.")
        if not self._is_password_secure(password):
            raise ValueError("Password does not meet security criteria.")
        password_hash = self._hash_password(password)
        return self._user_repository.create_user(email, password_hash)

    def _is_password_secure(self, password: str) -> bool:
        logger.debug("Validating password security criteria")
        return (
            len(password) >= 8
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
        )

    def _hash_password(self, password: str) -> str:
        logger.debug("Hashing password with SHA256")
        return hashlib.sha256(password.encode("utf-8")).hexdigest()