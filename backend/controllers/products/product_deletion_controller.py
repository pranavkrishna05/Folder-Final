from flask import Blueprint, jsonify, request
import logging
from backend.services.product_catalog.product_deletion_service import ProductDeletionService

product_delete_bp = Blueprint("product_delete", __name__)
logger = logging.getLogger(__name__)

def init_product_deletion_routes(service: ProductDeletionService) -> Blueprint:
    @product_delete_bp.route("/<int:product_id>/delete", methods=["DELETE"])
    def delete_product(product_id: int) -> tuple:
        data = request.get_json(force=True)
        is_admin = bool(data.get("is_admin", False))
        confirmation = bool(data.get("confirm", False))
        try:
            service.delete_product(product_id, is_admin, confirmation)
            return jsonify({"message": f"Product {product_id} deleted successfully"}), 200
        except PermissionError as pe:
            logger.warning("Unauthorized deletion attempt for product_id=%s", product_id)
            return jsonify({"error": str(pe)}), 403
        except ValueError as ve:
            logger.warning("Deletion validation error: %s", ve)
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logger.error("Unexpected error deleting product: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return product_delete_bp