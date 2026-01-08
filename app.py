import logging
from flask import Flask
from backend.config.settings import settings
from backend.repositories.users.user_repository import UserRepository
from backend.repositories.users.password_reset_repository import PasswordResetRepository
from backend.services.user_management.password_reset_service import PasswordResetService
from backend.controllers.users.password_reset_controller import init_password_reset_routes

def create_app() -> Flask:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    user_repo = UserRepository(settings.DATABASE_PATH)
    reset_repo = PasswordResetRepository(settings.DATABASE_PATH)
    reset_service = PasswordResetService(user_repo, reset_repo)

    app.register_blueprint(init_password_reset_routes(reset_service), url_prefix="/api/users")

    @app.route("/health", methods=["GET"])
    def health_check() -> dict:
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=settings.DEBUG)