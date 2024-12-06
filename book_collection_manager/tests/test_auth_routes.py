import pytest
from flask import Flask
from models.user_model import db, create_user
from auth_routes import auth_bp


@pytest.fixture
def app():
    """Fixture to create a Flask app instance for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    """Fixture to provide a test client."""
    return app.test_client()


@pytest.fixture
def sample_user():
    """Fixture to create a sample user for testing."""
    return {"username": "testuser", "password": "testpassword"}


##################################################
# Health Check Test Cases
##################################################

def test_health(client):
    """Test the /health-check route."""
    response = client.get('/api/health-check')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


##################################################
# User Authentication Test Cases
##################################################

def test_create_account_success(client, sample_user):
    """Test successful account creation."""
    response = client.post('/api/create-account', json=sample_user)
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'


def test_create_account_missing_fields(client):
    """Test account creation with missing fields."""
    response = client.post('/api/create-account', json={"username": "testuser"})
    assert response.status_code == 400
    assert response.json['error'] == 'Username and password are required'


def test_login_success(client, sample_user):
    """Test successful user login."""
    client.post('/api/create-account', json=sample_user)
    response = client.post('/api/login', json=sample_user)
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'


def test_login_invalid_credentials(client, sample_user):
    """Test login with invalid credentials."""
    client.post('/api/create-account', json=sample_user)
    response = client.post('/api/login', json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid username or password'


def test_update_password_success(client, sample_user):
    """Test successful password update."""
    client.post('/api/create-account', json=sample_user)
    response = client.put('/api/update-password', json={"username": "testuser", "new_password": "newpassword"})
    assert response.status_code == 200
    assert response.json['message'] == 'Password updated successfully'


def test_update_password_user_not_found(client):
    """Test updating password for a non-existent user."""
    response = client.put('/api/update-password', json={"username": "nonexistent", "new_password": "newpassword"})
    assert response.status_code == 404
    assert response.json['error'] == 'User not found'


def test_update_password_missing_fields(client):
    """Test password update with missing fields."""
    response = client.put('/api/update-password', json={"username": "testuser"})
    assert response.status_code == 400
    assert response.json['error'] == 'Username and new password are required'
