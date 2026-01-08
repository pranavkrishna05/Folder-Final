import logging
from flask import Flask
from backend.config.settings import settings
from backend.repositories.products.product_repository import ProductRepository
from backend.services.product_catalog.product_deletion_service import ProductDeletionService
from backend.controllers.products.product_deletion_controller import init_product_deletion_routes

def create_app() -> Flask:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    product_repo = ProductRepository(settings.DATABASE_PATH)
    deletion_service = ProductDeletionService(product_repo)

    app.register_blueprint(init_product_deletion_routes(deletion_service), url_prefix="/api/products")

    @app.route("/health", methods=["GET"])
    def health() -> dict:
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=settings.DEBUG)