from flask import Blueprint, request, jsonify
import logging
from backend.services.product_catalog.product_update_service import ProductUpdateService

product_update_bp = Blueprint("product_update", __name__)
logger = logging.getLogger(__name__)

def init_product_update_routes(service: ProductUpdateService) -> Blueprint:
    @product_update_bp.route("/<int:product_id>/update", methods=["PUT"])
    def update_product(product_id: int) -> tuple:
        data = request.get_json(force=True)
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        is_admin = data.get("is_admin", False)
        try:
            product = service.update_product_details(
                product_id=product_id,
                name=name,
                description=description,
                price=float(price),
                is_admin=bool(is_admin),
            )
            return jsonify(product.__dict__), 200
        except PermissionError as pe:
            logger.warning("Unauthorized update attempt for product_id=%s", product_id)
            return jsonify({"error": str(pe)}), 403
        except ValueError as ve:
            logger.warning("Validation failed while updating product: %s", ve)
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logger.error("Unexpected error updating product: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return product_update_bp