import logging
from repositories.product_repository import ProductRepository
from models.product import Product

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def add_product(self, name: str, description: str, price: float, category: str) -> Product:
        logger.info("Validating product before creation")
        if not name or not description:
            raise ValueError("Product name and description cannot be empty.")
        if price is None or float(price) <= 0:
            raise ValueError("Product price must be a positive number.")
        existing = self._product_repository.find_by_name(name)
        if existing:
            raise ValueError("Product with the same name already exists.")
        return self._product_repository.create_product(name, description, float(price), category)