from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime