import logging
import signal
import sys
from flask import Flask, jsonify, request
from models.product import Product
from repositories.product_repository import ProductRepository
from services.products.product_update_service import ProductUpdateService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
product_service = ProductUpdateService(product_repository)

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    updated_by_admin = data.get("updated_by_admin", False)

    if not updated_by_admin:
        return jsonify({"error": "Only admin users can update products"}), 403

    try:
        product = product_service.update_product(product_id, name, description, price)
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
        }), 200
    except ValueError as e:
        logger.error(f"Product update error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Internal error: {e}")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for product update management")
    app.run(host="0.0.0.0", port=5000)