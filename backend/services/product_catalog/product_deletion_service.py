import logging
from backend.repositories.products.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductDeletionService:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    def delete_product(self, product_id: int, is_admin: bool, confirmation: bool) -> None:
        if not is_admin:
            raise PermissionError("Only admins can delete products")
        if not confirmation:
            raise ValueError("Product deletion requires explicit confirmation")
        product = self._product_repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if product.is_deleted:
            raise ValueError("Product is already deleted")
        logger.info("Admin deleting product id=%s", product_id)
        self._product_repo.soft_delete_product(product_id)