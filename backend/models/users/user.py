from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class User:
    id: int
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime