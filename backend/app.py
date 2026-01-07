import logging
import signal
import sys
from flask import Flask, jsonify, request
from models.user import User
from repositories.user_repository import UserRepository
from services.auth.profile_service import ProfileService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

user_repository = UserRepository()
profile_service = ProfileService(user_repository)

@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id: int) -> tuple:
    try:
        user = profile_service.get_profile(user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404
        return jsonify({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "preferences": user.preferences
        }), 200
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id: int) -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400
    try:
        user = profile_service.update_profile(user_id, data)
        return jsonify({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "preferences": user.preferences
        }), 200
    except ValueError as e:
        logger.error(f"Profile update error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for profile management")
    app.run(host="0.0.0.0", port=5000)