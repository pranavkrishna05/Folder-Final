import sqlite3
import logging
from typing import Optional, List
from models.cart_item import CartItem

logger = logging.getLogger(__name__)

class CartRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_cart_item(self, user_id: Optional[int], product_id: int) -> Optional[CartItem]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        if user_id is None:
            cursor.execute(
                "SELECT id, user_id, product_id, quantity, created_at, updated_at FROM cart WHERE user_id IS NULL AND product_id = ?",
                (product_id,),
            )
        else:
            cursor.execute(
                "SELECT id, user_id, product_id, quantity, created_at, updated_at FROM cart WHERE user_id = ? AND product_id = ?",
                (user_id, product_id),
            )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return CartItem(*row)

    def update_quantity(self, cart_item_id: int, quantity: int) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE cart SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (quantity, cart_item_id),
        )
        connection.commit()
        connection.close()

    def get_user_cart_items(self, user_id: Optional[int]) -> List[CartItem]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        if user_id is None:
            cursor.execute(
                "SELECT id, user_id, product_id, quantity, created_at, updated_at FROM cart WHERE user_id IS NULL"
            )
        else:
            cursor.execute(
                "SELECT id, user_id, product_id, quantity, created_at, updated_at FROM cart WHERE user_id = ?",
                (user_id,),
            )
        rows = cursor.fetchall()
        connection.close()
        return [CartItem(*r) for r in rows]