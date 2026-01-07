import logging
import signal
import sys
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from models.user import User
from models.password_reset import PasswordReset
from repositories.user_repository import UserRepository
from repositories.password_reset_repository import PasswordResetRepository
from services.auth.password_reset_service import PasswordResetService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

user_repository = UserRepository()
password_reset_repository = PasswordResetRepository()
password_reset_service = PasswordResetService(user_repository, password_reset_repository)

@app.route("/password-reset/request", methods=["POST"])
def request_password_reset() -> tuple:
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Email field is required"}), 400
    try:
        token = password_reset_service.initiate_reset(data["email"])
        return jsonify({"reset_token": token}), 200
    except ValueError as e:
        logger.error(f"Password reset request error: {e}")
        return jsonify({"error": str(e)}), 400

@app.route("/password-reset/confirm", methods=["POST"])
def confirm_password_reset() -> tuple:
    data = request.get_json()
    if not data or "token" not in data or "new_password" not in data:
        return jsonify({"error": "Token and new password fields are required"}), 400
    try:
        password_reset_service.complete_reset(data["token"], data["new_password"])
        return jsonify({"message": "Password reset successful"}), 200
    except ValueError as e:
        logger.error(f"Password reset confirmation error: {e}")
        return jsonify({"error": str(e)}), 400

def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for password reset management")
    app.run(host="0.0.0.0", port=5000)