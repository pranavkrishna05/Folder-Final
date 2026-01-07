import sqlite3
import logging
from typing import Optional
from models.product import Product

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def find_by_id(self, product_id: int) -> Optional[Product]:
        logger.info(f"Fetching product with id {product_id}")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, description, price, category, created_at, updated_at FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Product(*row)

    def update_product(self, product_id: int, name: str, description: str, price: float) -> Product:
        logger.info(f"Updating product ID {product_id}")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE products
            SET name = ?, description = ?, price = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (name, description, price, product_id),
        )
        connection.commit()
        cursor.execute(
            "SELECT id, name, description, price, category, created_at, updated_at FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            raise ValueError("Product not found after update.")
        return Product(*row)