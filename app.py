import logging
from flask import Flask
from backend.config.settings import settings
from backend.repositories.users.profile_repository import ProfileRepository
from backend.services.user_management.profile_service import ProfileService
from backend.controllers.users.profile_controller import init_profile_routes

def create_app() -> Flask:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    profile_repo = ProfileRepository(settings.DATABASE_PATH)
    profile_service = ProfileService(profile_repo)

    app.register_blueprint(init_profile_routes(profile_service), url_prefix="/api/users")

    @app.route("/health", methods=["GET"])
    def health() -> dict:
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=settings.DEBUG)