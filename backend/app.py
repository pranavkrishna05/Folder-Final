import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from services.cart.cart_quantity_service import CartQuantityService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
cart_repository = CartRepository()
cart_quantity_service = CartQuantityService(cart_repository, product_repository)

@app.route("/cart/update", methods=["PATCH"])
def update_cart_quantity() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    new_quantity = data.get("quantity")

    try:
        updated_total = cart_quantity_service.update_quantity(user_id, product_id, new_quantity)
        logger.info("Cart updated successfully for product %s", product_id)
        return jsonify({
            "message": f"Quantity updated successfully for product {product_id}.",
            "updated_total_price": updated_total
        }), 200
    except ValueError as e:
        logger.error(f"Cart update validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error while updating cart quantity")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info("Received shutdown signal (%s), stopping application gracefully.", signal_number)
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for modifying cart quantities")
    app.run(host="0.0.0.0", port=5000)