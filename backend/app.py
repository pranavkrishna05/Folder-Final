import logging
import signal
import sys
from flask import Flask, jsonify, request
from repositories.product_repository import ProductRepository
from services.products.product_search_service import ProductSearchService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

product_repository = ProductRepository()
search_service = ProductSearchService(product_repository)

@app.route("/products/search", methods=["GET"])
def search_products() -> tuple:
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    page = int(request.args.get("page", "1"))
    per_page = int(request.args.get("per_page", "10"))

    try:
        results, total = search_service.search_products(query, category, page, per_page)
        response = {
            "total": total,
            "page": page,
            "per_page": per_page,
            "results": [r.__dict__ for r in results],
        }
        logger.info("Search executed successfully with query '%s'", query)
        return jsonify(response), 200
    except ValueError as e:
        logger.error(f"Search validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Search failed unexpectedly")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for product search")
    app.run(host="0.0.0.0", port=5000)