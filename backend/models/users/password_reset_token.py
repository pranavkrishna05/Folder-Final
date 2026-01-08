from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PasswordResetToken:
    id: int
    user_id: int
    token: str
    expires_at: datetime
    used: bool
    created_at: datetime