import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.product_repository import ProductRepository
from services.products.product_delete_service import ProductDeleteService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
product_delete_service = ProductDeleteService(product_repository)

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> tuple:
    data = request.get_json() or {}
    confirm = data.get("confirm", False)
    is_admin = data.get("is_admin", False)

    if not is_admin:
        return jsonify({"error": "Only admins can delete products."}), 403
    if not confirm:
        return jsonify({"error": "Deletion must be confirmed."}), 400
    try:
        product_delete_service.delete_product(product_id)
        logger.info("Product %s deleted successfully.", product_id)
        return jsonify({"message": f"Product {product_id} deleted successfully."}), 200
    except ValueError as e:
        logger.error(f"Product deletion failed: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Internal server error.")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for product deletion management")
    app.run(host="0.0.0.0", port=5000)