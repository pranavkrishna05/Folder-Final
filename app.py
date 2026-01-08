import logging
from flask import Flask
from backend.config.settings import settings
from backend.repositories.users.user_repository import UserRepository
from backend.services.user_management.registration_service import RegistrationService
from backend.controllers.users.registration_controller import init_registration_routes

def create_app() -> Flask:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    user_repository = UserRepository(settings.DATABASE_PATH)
    registration_service = RegistrationService(user_repository)
    app.register_blueprint(init_registration_routes(registration_service), url_prefix="/api/users")

    @app.route("/health", methods=["GET"])
    def health_check() -> dict:
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=settings.DEBUG)