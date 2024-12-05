import pytest
from flask import Flask
from models.book_model import Book, db
from book_routes import books_bp


@pytest.fixture
def app():
    """Fixture to create a Flask app instance for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(books_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    """Fixture to provide a test client."""
    return app.test_client()


@pytest.fixture
def sample_book():
    """Fixture to provide a sample book for testing."""
    return {
        "title": "Sample Book",
        "author": "Sample Author",
        "year": "2024",
        "status": "unread",
        "cover_image": None,
        "summary": None
    }


##################################################
# Health Check Test Cases
##################################################

def test_health(client):
    """Test the /health route."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {'status': 'App is running'}


##################################################
# Book Management Test Cases
##################################################

def test_add_book(client, sample_book):
    """Test adding a new book to the database."""
    response = client.post('/api/books', json=sample_book)
    assert response.status_code == 201
    assert response.json['message'] == 'Book added successfully'
    assert 'book_id' in response.json


def test_get_book(client, sample_book):
    """Test retrieving a book by ID."""
    # Add a book to the database
    response = client.post('/api/books', json=sample_book)
    book_id = response.json['book_id']

    # Retrieve the book
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 200
    assert response.json['title'] == sample_book['title']
    assert response.json['author'] == sample_book['author']
    assert response.json['year'] == sample_book['year']


def test_get_nonexistent_book(client):
    """Test retrieving a book that does not exist."""
    response = client.get('/api/books/999') # This is not a real book
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found'


def test_update_reading_status(client, sample_book):
    """Test updating the reading status of a book."""
    # Add a book to the database
    response = client.post('/api/books', json=sample_book)
    book_id = response.json['book_id']

    # Update the reading status
    response = client.put(f'/api/books/{book_id}', json={'status': 'read'})
    assert response.status_code == 200
    assert response.json['message'] == 'Reading status updated'

    # Verify the update
    response = client.get(f'/api/books/{book_id}')
    assert response.json['status'] == 'read'


def test_delete_book(client, sample_book):
    """Test deleting a book from the database."""
    # Add a book to the database
    response = client.post('/api/books', json=sample_book)
    book_id = response.json['book_id']

    # Delete the book
    response = client.delete(f'/api/books/{book_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Book deleted successfully'

    # Verify the deletion
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 404


##################################################
# Google Books API Integration Test Cases
##################################################

def test_get_book_details(client, monkeypatch):
    """Test retrieving book details from the Google Books API."""
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.json_data = {
                    'items': [{
                        'volumeInfo': {
                            'title': 'Mocked Book',
                            'authors': ['Mocked Author'],
                            'publishedDate': '2024',
                            'description': 'This is a mocked book.',
                            'imageLinks': {'thumbnail': 'http://example.com/mocked.jpg'}
                        }
                    }]
                }

            def json(self):
                return self.json_data

        return MockResponse()

    monkeypatch.setattr('requests.get', mock_get)

    response = client.get('/api/books/details?title=Mocked')
    assert response.status_code == 200
    assert response.json['title'] == 'Mocked Book'
    assert response.json['author'] == 'Mocked Author'
    assert response.json['published_date'] == '2024'
    assert response.json['summary'] == 'This is a mocked book.'
    assert response.json['cover_image'] == 'http://example.com/mocked.jpg'


def test_get_book_details_missing_title(client):
    """Test retrieving book details without a title parameter."""
    response = client.get('/api/books/details')
    assert response.status_code == 400
    assert response.json['error'] == 'Title is required'


def test_get_book_details_api_failure(client, monkeypatch):
    """Test handling an API failure when fetching book details."""
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 500

        return MockResponse()

    monkeypatch.setattr('requests.get', mock_get)

    response = client.get('/api/books/details?title=Mocked')
    assert response.status_code == 500
    assert response.json['error'] == 'Failed to fetch book details'
