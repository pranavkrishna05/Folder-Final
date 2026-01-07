import logging
import signal
import sys
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from models.user import User
from models.session import Session
from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository
from services.auth.login_service import LoginService

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

user_repository = UserRepository()
session_repository = SessionRepository()
login_service = LoginService(user_repository, session_repository)

@app.route("/login", methods=["POST"])
def login_user() -> tuple:
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    try:
        session = login_service.login(email, password)
        return jsonify({
            "session_token": session.token,
            "expires_at": session.expires_at.isoformat()
        }), 200
    except ValueError as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": str(e)}), 400


def shutdown_handler(signal_number, _frame):
    logger.info(f"Received shutdown signal ({signal_number}), stopping application gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    logger.info("Starting Flask application for user login")
    app.run(host="0.0.0.0", port=5000)