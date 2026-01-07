import sqlite3
import logging
from typing import Optional
from models.product import Product

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_by_id(self, product_id: int) -> Optional[Product]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, description, price, category_id, is_deleted, created_at, updated_at FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Product(*row)

    def update_category(self, product_id: int, category_id: int) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE products SET category_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (category_id, product_id),
        )
        connection.commit()
        connection.close()