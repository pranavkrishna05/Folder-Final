import sqlite3
from typing import Optional, List
from datetime import datetime
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
                "SELECT id, name, description, price, category_id, is_deleted, created_at, updated_at FROM products WHERE id=?",
                (product_id,),
            )
            row = cursor.fetchone()
            return Product(*row) if row else None

    def soft_delete_product(self, product_id: int) -> None:
        logger.info("Soft deleting product id=%s", product_id)
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE products SET is_deleted=1, updated_at=? WHERE id=?",
                (datetime.now(), product_id),
            )

    def list_active_products(self) -> List[Product]:
        logger.info("Listing all active products")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, description, price, category_id, is_deleted, created_at, updated_at FROM products WHERE is_deleted=0"
            )
            rows = cursor.fetchall()
            return [Product(*row) for row in rows]