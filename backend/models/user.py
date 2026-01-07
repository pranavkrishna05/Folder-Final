from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    full_name: str
    preferences: str
    created_at: datetime
    updated_at: datetime