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
            "SELECT id, name, description, price, category, is_deleted, created_at, updated_at FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Product(*row)

    def soft_delete_product(self, product_id: int) -> None:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE products SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (product_id,),
        )
        connection.commit()
        connection.close()
        logger.info("Product ID %s marked as deleted.", product_id)

    def exists(self, product_id: int) -> bool:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(1) FROM products WHERE id = ? AND is_deleted = 0",
            (product_id,),
        )
        count = cursor.fetchone()[0]
        connection.close()
        return count > 0