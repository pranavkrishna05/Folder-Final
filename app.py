import logging
from flask import Flask
from backend.config.settings import settings
from backend.repositories.users.user_repository import UserRepository
from backend.repositories.users.session_repository import SessionRepository
from backend.services.user_management.login_service import LoginService
from backend.controllers.users.login_controller import init_login_routes

def create_app() -> Flask:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    user_repo = UserRepository(settings.DATABASE_PATH)
    session_repo = SessionRepository(settings.DATABASE_PATH)
    login_service = LoginService(user_repo, session_repo)

    app.register_blueprint(init_login_routes(login_service), url_prefix="/api/users")

    @app.route("/health", methods=["GET"])
    def health() -> dict:
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=settings.DEBUG)