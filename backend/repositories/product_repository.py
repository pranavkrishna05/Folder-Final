import sqlite3
from typing import Optional
from models.product import Product
import logging

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_by_id(self, product_id: int) -> Optional[Product]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, description, price, category_id, is_deleted, created_at, updated_at FROM products WHERE id = ? AND is_deleted = 0",
            (product_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Product(*row)