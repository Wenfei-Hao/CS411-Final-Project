from flask import Blueprint, request, jsonify
from models.user_model import User, db
from utils.hash_utils import generate_salt, hash_password, verify_password
import logging

# Initialize logger
logger = logging.getLogger('auth_routes')

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health', methods=['GET'])
def health():
    """Health check route to confirm the app is running."""
    logger.info("Health check endpoint accessed.")
    return jsonify({'status': 'App is running'}), 200

@auth_bp.route('/create-account', methods=['POST'])
def create_account():
    """Create a new user account."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Account creation failed: Missing username or password.")
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        logger.warning(f"Account creation failed: Username '{username}' already exists.")
        return jsonify({'error': 'Username already exists'}), 400

    # Create user
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    user = User(username=username, salt=salt, hashed_password=hashed_password)
    db.session.add(user)
    db.session.commit()

    logger.info(f"Account created successfully for username: {username}.")
    return jsonify({'message': 'Account created successfully', 'user_id': user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Login failed: Missing username or password.")
        return jsonify({'error': 'Username and password are required'}), 400

    # Find user
    user = User.query.filter_by(username=username).first()
    if not user:
        logger.warning(f"Login failed: Username '{username}' not found.")
        return jsonify({'error': 'Invalid username or password'}), 401

    # Verify password
    if not verify_password(password, user.salt, user.hashed_password):
        logger.warning(f"Login failed: Invalid password for username '{username}'.")
        return jsonify({'error': 'Invalid username or password'}), 401
    
    logger.info(f"User '{username}' logged in successfully.")
    return jsonify({'message': 'Login successful'}), 200

@auth_bp.route('/update-password', methods=['PUT'])
def update_password():
    """Update the password for an existing user."""
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        logger.warning("Password update failed: Missing username or new password.")
        return jsonify({'error': 'Username and new password are required'}), 400

    # Find user
    user = User.query.filter_by(username=username).first()
    if not user:
        logger.warning(f"Password update failed: User '{username}' not found.")
        return jsonify({'error': 'User not found'}), 404

    # Update password
    user.salt = generate_salt()
    user.hashed_password = hash_password(new_password, user.salt)
    db.session.commit()

    logger.info(f"Password updated successfully for username: {username}.")
    return jsonify({'message': 'Password updated successfully'}), 200
