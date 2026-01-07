import sqlite3
from typing import List
from models.cart_item import CartItem

class CartRepository:
    def __init__(self, db_path: str = "database/app.db"):
        self._db_path = db_path

    def get_user_cart(self, user_id: int) -> List[CartItem]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, user_id, product_id, quantity, created_at, updated_at FROM cart WHERE user_id = ?",
            (user_id,),
        )
        rows = cursor.fetchall()
        connection.close()
        return [CartItem(*r) for r in rows]

    def save_user_cart_snapshot(self, user_id: int) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM saved_carts WHERE user_id = ?", (user_id,))
        cursor.execute(
            "INSERT INTO saved_carts (user_id, cart_data) SELECT ?, json_group_array(json_object('product_id', product_id, 'quantity', quantity)) FROM cart WHERE user_id = ?",
            (user_id, user_id),
        )
        connection.commit()
        connection.close()

    def load_user_cart_snapshot(self, user_id: int) -> List[tuple]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT cart_data FROM saved_carts WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        connection.close()
        if not row or not row[0]:
            return []
        import json
        return json.loads(row[0])