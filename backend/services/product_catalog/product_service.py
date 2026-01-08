import logging
from backend.repositories.products.product_repository import ProductRepository
from backend.repositories.products.category_repository import CategoryRepository
from backend.models.products.product import Product

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository) -> None:
        self._product_repo = product_repo
        self._category_repo = category_repo

    def add_product(self, name: str, description: str, price: float, category_name: str) -> Product:
        if not name or not description:
            raise ValueError("Product name and description are required")
        existing = self._product_repo.get_product_by_name(name)
        if existing:
            raise ValueError("Product name must be unique")
        category = self._category_repo.get_category_by_name(category_name)
        if not category:
            category = self._category_repo.create_category(category_name, f"Category for {category_name}")
        return self._product_repo.create_product(name, description, price, category.id)