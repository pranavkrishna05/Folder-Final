from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Product:
    id: int
    name: str
    description: str
    price: float
    category_id: int
    created_at: datetime
    updated_at: datetime