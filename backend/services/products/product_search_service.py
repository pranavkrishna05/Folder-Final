import logging
from math import ceil
from typing import List, Tuple
from models.product import Product
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductSearchService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def search_products(
        self, query: str, category: str, page: int, per_page: int
    ) -> Tuple[List[Product], int]:
        if page < 1 or per_page < 1:
            raise ValueError("Page and per_page must be positive integers.")

        offset = (page - 1) * per_page
        logger.info("Performing search: query=%s, category=%s, page=%d, per_page=%d", query, category, page, per_page)

        products, total = self._product_repository.search_products(query, category, offset, per_page)

        logger.info("Search results returned: %d item(s) of %d total", len(products), total)
        return products, total