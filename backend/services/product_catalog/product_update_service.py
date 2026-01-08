import logging
from backend.repositories.products.product_repository import ProductRepository
from backend.models.products.product import Product

logger = logging.getLogger(__name__)

class ProductUpdateService:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    def update_product_details(self, product_id: int, name: str, description: str, price: float, is_admin: bool) -> Product:
        if not is_admin:
            raise PermissionError("Only admin users can update product details")
        logger.info("Updating product with admin privileges: product_id=%s", product_id)
        existing = self._product_repo.get_product_by_id(product_id)
        if not existing:
            raise ValueError("Product not found")
        return self._product_repo.update_product(product_id, name or existing.name, description, price)