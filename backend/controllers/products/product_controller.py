from flask import Blueprint, request, jsonify
import logging
from backend.services.product_catalog.product_service import ProductService

product_bp = Blueprint("products", __name__)
logger = logging.getLogger(__name__)

def init_product_routes(service: ProductService) -> Blueprint:
    @product_bp.route("/add", methods=["POST"])
    def add_product() -> tuple:
        data = request.get_json(force=True)
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        category_name = data.get("category")
        if not all([name, description, price, category_name]):
            return jsonify({"error": "All fields are required"}), 400
        try:
            product = service.add_product(name, description, float(price), category_name)
            return jsonify({"id": product.id, "name": product.name, "category_id": product.category_id}), 201
        except ValueError as e:
            logger.warning("Product creation failed: %s", e)
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Unexpected error while adding product: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return product_bp