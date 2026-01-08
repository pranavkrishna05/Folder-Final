import sqlite3
from datetime import datetime
from typing import Optional, List
from backend.models.products.product import Product
import logging

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        logger.info("Fetching product by id=%s", product_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, description, price, category_id, created_at, updated_at FROM products WHERE id=?",
                (product_id,),
            )
            row = cursor.fetchone()
            return Product(*row) if row else None

    def update_product(self, product_id: int, name: str, description: str, price: float) -> Optional[Product]:
        if price <= 0:
            raise ValueError("Product price must be a numeric value greater than zero")
        if not description or description.strip() == "":
            raise ValueError("Description cannot be removed or empty")
        logger.info("Updating product id=%s", product_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE products
                SET name=?, description=?, price=?, updated_at=?
                WHERE id=?
                """,
                (name, description, price, datetime.now(), product_id),
            )
            conn.commit()
        return self.get_product_by_id(product_id)

    def list_products(self) -> List[Product]:
        logger.info("Listing all products")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price, category_id, created_at, updated_at FROM products")
            rows = cursor.fetchall()
            return [Product(*row) for row in rows]