from flask import Blueprint, request, jsonify
import logging
from backend.services.product_catalog.product_search_service import ProductSearchService

product_search_bp = Blueprint("product_search", __name__)
logger = logging.getLogger(__name__)

def init_product_search_routes(service: ProductSearchService) -> Blueprint:
    @product_search_bp.route("/search", methods=["GET"])
    def search_products() -> tuple:
        query = request.args.get("q", "")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        try:
            results = service.search(query, page, per_page)
            return jsonify({"results": results, "page": page, "per_page": per_page}), 200
        except ValueError as ve:
            logger.warning("Invalid search parameters: %s", ve)
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logger.error("Unexpected error during product search: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return product_search_bp