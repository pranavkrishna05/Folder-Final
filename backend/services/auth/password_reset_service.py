import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from repositories.user_repository import UserRepository
from repositories.password_reset_repository import PasswordResetRepository
from models.password_reset import PasswordReset

logger = logging.getLogger(__name__)

class PasswordResetService:
    def __init__(self, user_repo: UserRepository, password_reset_repo: PasswordResetRepository) -> None:
        self._user_repo = user_repo
        self._password_reset_repo = password_reset_repo
        self._expiry_hours = 24

    def initiate_reset(self, email: str) -> str:
        user = self._user_repo.find_by_email(email)
        if not user:
            raise ValueError("Email not registered.")
        token = secrets.token_urlsafe(48)
        expires_at = (datetime.utcnow() + timedelta(hours=self._expiry_hours)).isoformat()
        self._password_reset_repo.create_token(user.id, token, expires_at)
        logger.info(f"Password reset token created for user {email}")
        return token

    def complete_reset(self, token: str, new_password: str) -> None:
        reset_request = self._password_reset_repo.find_by_token(token)
        if not reset_request:
            raise ValueError("Invalid or non-existent token.")
        if reset_request.used:
            raise ValueError("Token already used.")
        if datetime.fromisoformat(reset_request.expires_at) < datetime.utcnow():
            raise ValueError("Token has expired.")
        hashed = self._hash_password(new_password)
        self._user_repo.update_password(reset_request.user_id, hashed)
        self._password_reset_repo.mark_used(token)
        logger.info("Password successfully reset for user id %s", reset_request.user_id)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()