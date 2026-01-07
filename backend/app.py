import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.cart_repository import CartRepository
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from services.cart.cart_persistence_service import CartPersistenceService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

user_repository = UserRepository()
product_repository = ProductRepository()
cart_repository = CartRepository()
cart_persistence_service = CartPersistenceService(cart_repository, product_repository, user_repository)

@app.route("/cart/save", methods=["POST"])
def save_cart_state() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    user_id = data.get("user_id")

    try:
        cart_persistence_service.save_cart_state(user_id)
        logger.info("Cart state saved successfully for user %s", user_id)
        return jsonify({"message": f"Cart state saved for user {user_id}"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error while saving user cart state.")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/cart/load", methods=["GET"])
def load_cart_state() -> tuple:
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id parameter required"}), 400
    try:
        cart_items, total_price = cart_persistence_service.load_cart_state(int(user_id))
        results = [
          {
            "product_id": item.product_id,
            "quantity": item.quantity
          } for item in cart_items
        ]
        response = {"total_price": total_price, "cart": results}
        return jsonify(response), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error while loading user cart state.")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info("Received shutdown signal (%s), stopping application gracefully.", signal_number)
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for cart persistence feature")
    app.run(host="0.0.0.0", port=5000)