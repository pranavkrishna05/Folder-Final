import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from services.products.category_service import CategoryService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

category_repository = CategoryRepository()
product_repository = ProductRepository()
category_service = CategoryService(category_repository, product_repository)

@app.route("/categories", methods=["POST"])
def create_category() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    name = data.get("name")
    parent_id = data.get("parent_id")

    try:
        category = category_service.create_category(name, parent_id)
        return jsonify({
            "id": category.id,
            "name": category.name,
            "parent_id": category.parent_id
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/categories/<int:category_id>/products/<int:product_id>", methods=["POST"])
def assign_product_category(category_id: int, product_id: int) -> tuple:
    try:
        category_service.assign_product_to_category(product_id, category_id)
        return jsonify({"message": f"Product {product_id} assigned to category {category_id}"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for product categorization")
    app.run(host="0.0.0.0", port=5000)