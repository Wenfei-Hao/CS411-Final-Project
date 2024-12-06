from flask import Blueprint, request, jsonify
from models.user_model import create_user, get_user_by_username, update_user_password
from utils.hash_utils import verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/create-account', methods=['POST'])
def create_account():
    """Handles user account creation.

    Expects a JSON payload with `username` and `password`. Creates a new user
    if the username is unique.

    Returns:
        Response: A JSON response with a success message and status code 201,
        or an error message with status code 400.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    success, message = create_user(username, password)
    if success:
        return jsonify({"message": message}), 201
    return jsonify({"error": message}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handles user login.

    Expects a JSON payload with `username` and `password`. Verifies the
    credentials against stored user data.

    Returns:
        Response: A JSON response with a success message and status code 200,
        or an error message with status code 401.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = get_user_by_username(username)
    if user and verify_password(password, user.salt, user.hashed_password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route('/update-password', methods=['PUT'])
def update_password():
    """Handles user password updates.

    Expects a JSON payload with `username` and `new_password`. Updates the
    password for the specified user if the user exists.

    Returns:
        Response: A JSON response with a success message and status code 200,
        or an error message with status code 404.
    """
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({"error": "Username and new password are required"}), 400

    success, message = update_user_password(username, new_password)
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"error": message}), 404
