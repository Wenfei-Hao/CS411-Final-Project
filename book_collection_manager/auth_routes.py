from flask import Blueprint, request, jsonify
from models.user_model import User, db
from utils.hash_utils import generate_salt, hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health', methods=['GET'])
def health():
    """Health check route to confirm the app is running."""
    return jsonify({'status': 'App is running'}), 200

@auth_bp.route('/create-account', methods=['POST'])
def create_account():
    """Create a new user account."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Create user
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    user = User(username=username, salt=salt, hashed_password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully', 'user_id': user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Find user
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Verify password
    if not verify_password(password, user.salt, user.hashed_password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

@auth_bp.route('/update-password', methods=['PUT'])
def update_password():
    """Update the password for an existing user."""
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({'error': 'Username and new password are required'}), 400

    # Find user
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update password
    user.salt = generate_salt()
    user.hashed_password = hash_password(new_password, user.salt)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200


@auth_bp.route('/delete-account/<int:user_id>', methods=['DELETE'])
def delete_account(user_id):
    """Delete a user account."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Account deleted successfully'}), 200
