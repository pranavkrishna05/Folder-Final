import logging
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductDeleteService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def delete_product(self, product_id: int) -> None:
        logger.info("Attempting to delete product ID %s", product_id)
        if not self._product_repository.exists(product_id):
            raise ValueError("Product not found or already deleted.")
        self._product_repository.soft_delete_product(product_id)
        logger.info("Deletion successful for product ID %s", product_id)