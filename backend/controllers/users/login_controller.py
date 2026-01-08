from flask import Blueprint, request, jsonify
import logging
from backend.services.user_management.login_service import LoginService

login_bp = Blueprint("login", __name__)
logger = logging.getLogger(__name__)

def init_login_routes(service: LoginService) -> Blueprint:
    @login_bp.route("/login", methods=["POST"])
    def login_user() -> tuple:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        try:
            session = service.login(email, password)
            return jsonify({"token": session.token, "expires_at": session.expires_at.isoformat()}), 200
        except ValueError as e:
            logger.warning("Login failed: %s", e)
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            logger.error("Unexpected error during login: %s", e)
            return jsonify({"error": "Internal server error"}), 500
    return login_bp