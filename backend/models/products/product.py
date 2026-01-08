from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Product:
    id: int
    name: str
    description: str
    price: float
    category_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime