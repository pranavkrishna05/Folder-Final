import logging
from typing import Optional
from models.category import Category
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class CategoryService:
    def __init__(self, category_repository: CategoryRepository, product_repository: ProductRepository) -> None:
        self._category_repo = category_repository
        self._product_repo = product_repository

    def create_category(self, name: str, parent_id: Optional[int]) -> Category:
        logger.info("Creating category: %s", name)
        if not name:
            raise ValueError("Category name cannot be empty.")
        existing = self._category_repo.find_by_name(name)
        if existing:
            raise ValueError("Category name must be unique.")
        if parent_id is not None:
            parent = self._category_repo.find_by_id(parent_id)
            if not parent:
                raise ValueError("Parent category does not exist.")
        return self._category_repo.create(name, parent_id)

    def assign_product_to_category(self, product_id: int, category_id: int) -> None:
        product = self._product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")
        category = self._category_repo.find_by_id(category_id)
        if not category:
            raise ValueError("Category not found.")
        self._product_repo.update_category(product_id, category_id)
        logger.info("Product %s assigned to category %s", product_id, category_id)