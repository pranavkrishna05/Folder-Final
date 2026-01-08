import logging
from backend.repositories.users.user_repository import UserRepository
from backend.repositories.users.session_repository import SessionRepository
from backend.services.auth.password_utils import verify_password
from backend.models.users.session import Session

MAX_FAILED_ATTEMPTS = 5

logger = logging.getLogger(__name__)

class LoginService:
    def __init__(self, user_repository: UserRepository, session_repository: SessionRepository) -> None:
        self._user_repo = user_repository
        self._session_repo = session_repository

    def login(self, email: str, password: str) -> Session:
        user = self._user_repo.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        if user.is_locked:
            raise ValueError("Account is locked due to multiple failed attempts")
        if not verify_password(password, user.password_hash):
            failed_attempts = user.failed_login_attempts + 1
            is_locked = failed_attempts >= MAX_FAILED_ATTEMPTS
            self._user_repo.update_login_attempts(user.id, failed_attempts, is_locked)
            raise ValueError("Invalid email or password")
        self._user_repo.update_login_attempts(user.id, 0, False)
        self._user_repo.update_last_login(user.id)
        session = self._session_repo.create_session(user.id)
        return session