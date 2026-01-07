import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from services.cart.cart_removal_service import CartRemovalService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
cart_repository = CartRepository()
cart_removal_service = CartRemovalService(cart_repository, product_repository)

@app.route("/cart/remove", methods=["DELETE"])
def remove_from_cart() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    confirm = data.get("confirm", False)

    if not confirm:
        return jsonify({"error": "Deletion must be confirmed."}), 400

    try:
        updated_total = cart_removal_service.remove_product_from_cart(user_id, product_id)
        return jsonify({
            "message": f"Product {product_id} removed successfully.",
            "updated_total_price": updated_total
        }), 200
    except ValueError as e:
        logger.error(f"Cart removal validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected server error while removing product from cart.")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info("Received shutdown signal (%s), stopping application gracefully.", signal_number)
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for removing products from cart")
    app.run(host="0.0.0.0", port=5000)