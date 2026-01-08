import sqlite3
from typing import List
from backend.models.products.product import Product
import logging

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn

    def search_products(self, query: str, page: int, per_page: int) -> List[dict]:
        logger.info("Searching products with query='%s', page=%s", query, page)
        offset = (page - 1) * per_page
        pattern = f"%{query.lower()}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT p.id, p.name, p.description, p.price, c.name AS category_name,
                       p.created_at, p.updated_at
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.is_deleted = 0
                AND (LOWER(p.name) LIKE ? OR LOWER(p.description) LIKE ? OR LOWER(c.name) LIKE ?)
                ORDER BY p.updated_at DESC
                LIMIT ? OFFSET ?
                """,
                (pattern, pattern, pattern, per_page, offset),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "description": row["description"],
                    "price": row["price"],
                    "category_name": row["category_name"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                for row in rows
            ]