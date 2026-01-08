from flask import Blueprint, request, jsonify
import logging
from backend.services.user_management.password_reset_service import PasswordResetService

password_reset_bp = Blueprint("password_reset", __name__)
logger = logging.getLogger(__name__)

def init_password_reset_routes(service: PasswordResetService) -> Blueprint:
    @password_reset_bp.route("/password/forgot", methods=["POST"])
    def forgot_password() -> tuple:
        data = request.get_json(force=True)
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email is required"}), 400
        try:
            token = service.initiate_password_reset(email)
            # In production, email would be sent
            return jsonify({"message": "Password reset link sent", "token": token}), 200
        except ValueError as e:
            logger.warning("Password reset initiation failed: %s", e)
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Unexpected error during password reset initiation: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    @password_reset_bp.route("/password/reset", methods=["POST"])
    def reset_password() -> tuple:
        data = request.get_json(force=True)
        token = data.get("token")
        new_password = data.get("new_password")
        if not token or not new_password:
            return jsonify({"error": "Token and new password are required"}), 400
        try:
            service.reset_password(token, new_password)
            return jsonify({"message": "Password has been reset successfully"}), 200
        except ValueError as e:
            logger.warning("Password reset failed: %s", e)
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Unexpected error during password reset: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return password_reset_bp