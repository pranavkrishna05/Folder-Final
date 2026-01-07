import logging
from models.product import Product
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductUpdateService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def update_product(self, product_id: int, name: str | None, description: str | None, price: float | None) -> Product:
        logger.info(f"Starting validation for product update ID {product_id}")
        product = self._product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        updated_name = name if name else product.name
        updated_description = description if description else product.description
        updated_price = price if price is not None else product.price

        if not updated_description:
            raise ValueError("Product description cannot be empty.")
        if updated_price is None or float(updated_price) <= 0:
            raise ValueError("Product price must be a numeric and positive value.")
        if not updated_name:
            raise ValueError("Product name cannot be empty.")

        logger.info(f"Updating product with validated fields for ID {product_id}")
        return self._product_repository.update_product(product_id, updated_name, updated_description, float(updated_price))