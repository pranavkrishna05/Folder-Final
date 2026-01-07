import logging
import signal
import sys
from flask import Flask, jsonify, request
from models.user import User
from repositories.user_repository import UserRepository
from services.auth.user_service import UserService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

user_repository = UserRepository()
user_service = UserService(user_repository)


@app.route("/register", methods=["POST"])
def register_user() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    try:
        user = user_service.register_user(email, password)
        return jsonify({"id": user.id, "email": user.email}), 201
    except ValueError as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"error": str(e)}), 400


def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=5000)