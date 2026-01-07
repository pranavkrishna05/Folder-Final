import sqlite3
import logging
from typing import List, Tuple
from models.product import Product

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def search_products(self, query: str, category: str, offset: int, limit: int) -> Tuple[List[Product], int]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()

        query_text = "SELECT id, name, description, price, category, is_deleted, created_at, updated_at FROM products WHERE is_deleted = 0"
        params: list[str] = []

        if query:
            query_text += " AND (name LIKE ? OR description LIKE ?)"
            like_query = f"%{query}%"
            params.extend([like_query, like_query])
        if category:
            query_text += " AND category = ?"
            params.append(category)

        count_query = f"SELECT COUNT(1) FROM ({query_text})"
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()[0]

        query_text += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(query_text, tuple(params))

        rows = cursor.fetchall()
        connection.close()

        results = [Product(*row) for row in rows]
        return results, total