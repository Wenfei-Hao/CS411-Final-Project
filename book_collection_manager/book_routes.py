from flask import Blueprint, request, jsonify, current_app
import requests
from models.book_model import Book, db

books_bp = Blueprint('books', __name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


@books_bp.route('/health', methods=['GET'])
def health():
    """Health check route to confirm the app is running."""
    current_app.logger.info("Health check endpoint accessed in book_routes.")
    return jsonify({"status": "healthy"}), 200


@books_bp.route('/books', methods=['POST'])
def add_book():
    """Add a new book to the database."""
    current_app.logger.info("Attempting to add a new book.")
    data = request.json
    title = data.get('title')
    author = data.get('author')
    year = data.get('year', '')
    user_id = data.get('user_id', 1)

    if not title or not author:
        current_app.logger.warning("Failed to add book: Missing title or author.")
        return jsonify({'error': 'Title and Author are required'}), 400

    try:
        book = Book(title=title, author=author, year=year, user_id=user_id)
        db.session.add(book)
        db.session.commit()
        current_app.logger.info(f"Book added successfully: {title} by {author}, ID: {book.id}")
        return jsonify({'message': 'Book added successfully', 'book_id': book.id}), 201
    except Exception as e:
        current_app.logger.error(f"Error adding book: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieve a book by its ID."""
    current_app.logger.info(f"Attempting to retrieve book with ID: {book_id}")
    book = db.session.get(Book, book_id)
    if not book:
        current_app.logger.warning(f"Book with ID {book_id} not found.")
        return jsonify({'error': 'Book not found'}), 404

    current_app.logger.info(f"Book retrieved: {book.title} by {book.author}, ID: {book.id}")
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'status': book.status,
        'cover_image': book.cover_image,
        'summary': book.summary
    })


@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_reading_status(book_id):
    """Update the reading status of a book."""
    current_app.logger.info(f"Attempting to update reading status for book ID: {book_id}")
    book = db.session.get(Book, book_id)
    if not book:
        current_app.logger.warning(f"Book with ID {book_id} not found.")
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    status = data.get('status')
    if status not in ['read', 'unread']:
        current_app.logger.warning(f"Invalid status '{status}' provided for book ID: {book_id}")
        return jsonify({'error': 'Invalid status. Use "read" or "unread".'}), 400

    book.status = status
    db.session.commit()
    current_app.logger.info(f"Reading status updated to '{status}' for book ID: {book_id}")
    return jsonify({'message': 'Reading status updated'})


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the database."""
    current_app.logger.info(f"Attempting to delete book with ID: {book_id}")
    book = db.session.get(Book, book_id)
    if not book:
        current_app.logger.warning(f"Book with ID {book_id} not found for deletion.")
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    current_app.logger.info(f"Book with ID {book_id} deleted successfully.")
    return jsonify({'message': 'Book deleted successfully'})


@books_bp.route('/books/details', methods=['GET'])
def get_book_details():
    """Fetch book details from the Google Books API."""
    title = request.args.get('title')
    if not title:
        current_app.logger.warning("Book details fetch failed: No title provided.")
        return jsonify({'error': 'Title is required'}), 400

    current_app.logger.info(f"Fetching details from Google Books API for title: {title}")
    response = requests.get(GOOGLE_BOOKS_API_URL, params={'q': title})
    if response.status_code != 200:
        current_app.logger.error(f"Failed to fetch book details: API returned {response.status_code}")
        return jsonify({'error': 'Failed to fetch book details'}), 500

    data = response.json()
    if 'items' not in data or not data['items']:
        current_app.logger.warning(f"No details found for title: {title}")
        return jsonify({'error': 'No book details found'}), 404

    book_data = data['items'][0]['volumeInfo']
    current_app.logger.info(f"Details fetched for title: {title}")
    return jsonify({
        'title': book_data.get('title'),
        'author': ', '.join(book_data.get('authors', [])),
        'published_date': book_data.get('publishedDate'),
        'summary': book_data.get('description'),
        'cover_image': book_data.get('imageLinks', {}).get('thumbnail')
    })


@books_bp.route('/books/collection', methods=['GET'])
def get_collection():
    """Retrieve the user's book collection."""
    user_id = request.args.get('user_id')
    if not user_id:
        current_app.logger.warning("Attempted to retrieve collection without user_id.")
        return jsonify({'error': 'user_id is required'}), 400

    current_app.logger.info(f"Retrieving book collection for user_id: {user_id}")
    user_books = Book.query.filter_by(user_id=user_id).all()

    book_list = [{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'year': b.year,
        'status': b.status
    } for b in user_books]

    current_app.logger.info(f"Collection retrieved for user_id: {user_id}, total books: {len(book_list)}")
    return jsonify({'collection': book_list}), 200
