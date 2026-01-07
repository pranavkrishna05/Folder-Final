import sqlite3
import logging
from typing import Optional
from models.category import Category

logger = logging.getLogger(__name__)

class CategoryRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def create(self, name: str, parent_id: Optional[int]) -> Category:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
            (name, parent_id),
        )
        connection.commit()
        new_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, name, parent_id, created_at, updated_at FROM categories WHERE id = ?",
            (new_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            raise ValueError("Failed to create category.")
        return Category(*row)

    def find_by_name(self, name: str) -> Optional[Category]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, parent_id, created_at, updated_at FROM categories WHERE name = ?",
            (name,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Category(*row)

    def find_by_id(self, category_id: int) -> Optional[Category]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, parent_id, created_at, updated_at FROM categories WHERE id = ?",
            (category_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Category(*row)