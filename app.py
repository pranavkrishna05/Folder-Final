import logging
from flask import Flask
from backend.config.settings import settings
from backend.repositories.products.product_repository import ProductRepository
from backend.repositories.products.category_repository import CategoryRepository
from backend.services.product_catalog.product_service import ProductService
from backend.controllers.products.product_controller import init_product_routes

def create_app() -> Flask:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    product_repo = ProductRepository(settings.DATABASE_PATH)
    category_repo = CategoryRepository(settings.DATABASE_PATH)
    product_service = ProductService(product_repo, category_repo)

    app.register_blueprint(init_product_routes(product_service), url_prefix="/api/products")

    @app.route("/health", methods=["GET"])
    def health() -> dict:
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=settings.DEBUG)