from flask import Blueprint, jsonify, request
import logging
from backend.services.user_management.profile_service import ProfileService

profile_bp = Blueprint("profile", __name__)
logger = logging.getLogger(__name__)

def init_profile_routes(service: ProfileService) -> Blueprint:
    @profile_bp.route("/<int:user_id>/profile", methods=["GET"])
    def get_profile(user_id: int) -> tuple:
        try:
            profile = service.get_user_profile(user_id)
            return jsonify(profile.__dict__), 200
        except ValueError as e:
            logger.warning("Profile not found for user_id=%s", user_id)
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error("Unexpected error fetching profile: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    @profile_bp.route("/<int:user_id>/profile", methods=["PUT"])
    def update_profile(user_id: int) -> tuple:
        data = request.get_json(force=True)
        try:
            profile = service.update_user_profile(
                user_id=user_id,
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone_number=data.get("phone_number"),
                address=data.get("address"),
                preferences=data.get("preferences"),
            )
            return jsonify(profile.__dict__), 200
        except ValueError as e:
            logger.warning("Profile update failed for user_id=%s: %s", user_id, e)
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error("Unexpected error updating profile: %s", e)
            return jsonify({"error": "Internal server error"}), 500

    return profile_bp