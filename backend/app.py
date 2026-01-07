import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from services.cart.cart_service import CartService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
cart_repository = CartRepository()
cart_service = CartService(cart_repository, product_repository)

@app.route("/cart/add", methods=["POST"])
def add_to_cart() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    user_id = data.get("user_id")  # None for guest users
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    try:
        cart_item = cart_service.add_product_to_cart(user_id, product_id, quantity)
        return jsonify({
            "cart_id": cart_item.cart_id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        }), 201
    except ValueError as e:
        logger.error(f"Add to cart validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error while adding to cart.")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for shopping cart functionality")
    app.run(host="0.0.0.0", port=5000)