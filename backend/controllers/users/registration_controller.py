from flask import Blueprint, request, jsonify
from backend.services.user_management.registration_service import RegistrationService
import logging

registration_bp = Blueprint("registration", __name__)
logger = logging.getLogger(__name__)

def init_registration_routes(service: RegistrationService) -> Blueprint:
    @registration_bp.route("/register", methods=["POST"])
    def register_user() -> tuple:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        try:
            user = service.register_user(email, password)
            return jsonify({"id": user.id, "email": user.email}), 201
        except ValueError as e:
            logger.warning("User registration failed: %s", e)
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Unexpected error during registration: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return registration_bp