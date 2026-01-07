import sqlite3
import logging
from typing import Optional
from models.product import Product

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self, db_path: str = "database/app.db") -> None:
        self._db_path = db_path

    def create_product(self, name: str, description: str, price: float, category: str) -> Product:
        logger.info("Creating product in the database")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, category) VALUES (?, ?, ?, ?)",
            (name, description, price, category),
        )
        connection.commit()
        product_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, name, description, price, category, created_at, updated_at FROM products WHERE id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            raise ValueError("Failed to create product.")
        return Product(*row)

    def find_by_name(self, name: str) -> Optional[Product]:
        logger.info(f"Checking if product exists by name: {name}")
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, description, price, category, created_at, updated_at FROM products WHERE name = ?",
            (name,),
        )
        row = cursor.fetchone()
        connection.close()
        if not row:
            return None
        return Product(*row)