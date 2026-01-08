from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Session:
    id: int
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime