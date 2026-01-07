from dataclasses import dataclass
from datetime import datetime

@dataclass
class CartItem:
    id: int
    user_id: int | None
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime