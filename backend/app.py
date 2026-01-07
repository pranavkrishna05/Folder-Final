import logging
import signal
import sys
from flask import Flask, jsonify, request
from models.product import Product
from repositories.product_repository import ProductRepository
from services.products.product_service import ProductService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
product_service = ProductService(product_repository)

@app.route("/products", methods=["POST"])
def add_product() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    category = data.get("category")
    try:
        product = product_service.add_product(name, description, price, category)
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category
        }), 201
    except ValueError as e:
        logger.error(f"Product creation error: {e}")
        return jsonify({"error": str(e)}), 400

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for product management")
    app.run(host="0.0.0.0", port=5000)