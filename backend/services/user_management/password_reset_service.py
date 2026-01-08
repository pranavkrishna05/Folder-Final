import logging
from backend.repositories.users.user_repository import UserRepository
from backend.repositories.users.password_reset_repository import PasswordResetRepository
from backend.services.auth.password_utils import hash_password
from backend.repositories.users.password_reset_repository import PasswordResetToken

logger = logging.getLogger(__name__)

class PasswordResetService:
    def __init__(self, user_repo: UserRepository, reset_repo: PasswordResetRepository) -> None:
        self._user_repo = user_repo
        self._reset_repo = reset_repo

    def initiate_password_reset(self, email: str) -> str:
        user = self._user_repo.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        token_obj = self._reset_repo.create_reset_token(user.id)
        logger.info("Password reset token created for user_id=%s", user.id)
        # In production, an email would be sent here with the token
        return token_obj.token

    def reset_password(self, token: str, new_password: str) -> None:
        token_obj = self._reset_repo.get_valid_token(token)
        if not token_obj:
            raise ValueError("Invalid or expired token")
        new_hash = hash_password(new_password)
        with self._user_repo._get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (new_hash, token_obj.user_id),
            )
        self._reset_repo.mark_token_as_used(token)
        logger.info("Password successfully reset for user_id=%s", token_obj.user_id)