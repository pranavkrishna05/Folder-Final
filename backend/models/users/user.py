from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class User:
    id: int
    email: str
    password_hash: str
    failed_login_attempts: int
    is_locked: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime