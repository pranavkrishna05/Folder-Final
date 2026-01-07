import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from models.session import Session
from models.user import User
from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository

logger = logging.getLogger(__name__)

class LoginService:
    def __init__(self, user_repo: UserRepository, session_repo: SessionRepository) -> None:
        self._user_repo = user_repo
        self._session_repo = session_repo
        self._max_attempts = 5
        self._session_duration_minutes = 30

    def login(self, email: str, password: str) -> Session:
        user = self._user_repo.find_by_email(email)
        if not user:
            raise ValueError("Invalid credentials.")
        if user.is_locked:
            raise ValueError("Account is locked due to repeated failed attempts.")
        hashed_input = self._hash_password(password)
        if hashed_input != user.password_hash:
            new_attempts = user.failed_attempts + 1
            lock = new_attempts >= self._max_attempts
            self._user_repo.update_failed_attempts(email, new_attempts, lock)
            logger.warning(f"Failed login attempt {new_attempts} for {email}")
            raise ValueError("Invalid credentials.")
        self._user_repo.update_last_login(user.id)
        token = secrets.token_hex(32)
        expires_at = datetime.utcnow() + timedelta(minutes=self._session_duration_minutes)
        logger.info(f"User {email} logged in successfully, session issued.")
        return self._session_repo.create_session(user.id, token, expires_at)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()