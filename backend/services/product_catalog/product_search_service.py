import logging
from backend.repositories.products.product_repository import ProductRepository
from typing import List, Dict

logger = logging.getLogger(__name__)

class ProductSearchService:
    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    def search(self, query: str, page: int = 1, per_page: int = 10) -> List[Dict[str, str]]:
        if not query or query.strip() == "":
            raise ValueError("Search term cannot be empty")
        if page < 1 or per_page < 1:
            raise ValueError("Invalid pagination parameters")
        logger.info("Performing product search with query='%s'", query)
        results = self._product_repo.search_products(query, page, per_page)
        # Optionally highlight matched query term
        lower_query = query.lower()
        for result in results:
            if lower_query in result["name"].lower():
                result["name"] = result["name"].replace(query, f"*{query}*")
            if lower_query in result["description"].lower():
                result["description"] = result["description"].replace(query, f"*{query}*")
        return results