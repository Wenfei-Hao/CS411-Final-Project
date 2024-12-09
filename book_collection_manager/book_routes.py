from flask import Blueprint, request, jsonify, current_app
import requests
from models.book_model import Book, db
import logging

# Initialize logger
logger = logging.getLogger('auth_routes')

books_bp = Blueprint('books', __name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


@books_bp.route('/health', methods=['GET'])
def health():
    """Health check route to confirm the app is running."""
    current_app.logger.info("Health check route accessed")
    return jsonify({'status': 'App is running'}), 200


@books_bp.route('/books', methods=['POST'])
def add_book():
    """Add a new book to the database."""
    current_app.logger.info("Attempting to add a new book.")
    data = request.json
    title = data.get('title')
    author = data.get('author')
    year = data.get('year', '')

    if not title or not author:
        current_app.logger.warning("Book addition failed: Missing title or author.")
        return jsonify({'error': 'Title and Author are required'}), 400

    book = Book(title=title, author=author, year=year)
    db.session.add(book)
    db.session.commit()

    current_app.logger.info(f"Book added successfully: {title} by {author}.")
    return jsonify({'message': 'Book added successfully', 'book_id': book.id}), 201


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieve a book by its ID."""
    current_app.logger.info("Attempting to get a book.")
    book = db.session.get(Book, book_id)
    if not book:
        current_app.logger.warning(f"Book retrieval failed: Book ID '{book_id}' not found.")
        return jsonify({'error': 'Book not found'}), 404
    
    current_app.logger.info(f"Book retrieved successfully: {book.title} by {book.author}.")
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
    current_app.logger.info("Attempting to update the reading status of a book.")
    book = db.session.get(Book, book_id)
    if not book:
        current_app.logger.warning(f"Reading status update failed: Book ID '{book_id}' not found.")
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    status = data.get('status')
    if status not in ['read', 'unread']:
        current_app.logger.warning(f"Invalid reading status '{status}' provided for Book ID '{book_id}'.")
        return jsonify({'error': 'Invalid status. Use "read" or "unread".'}), 400

    book.status = status
    db.session.commit()

    current_app.logger.info(f"Reading status updated to '{status}' for Book ID '{book_id}'.")
    return jsonify({'message': 'Reading status updated'})


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the database."""
    current_app.logger.info("Attempting to delete a book.")
    book = db.session.get(Book, book_id)
    if not book:
        current_app.logger.warning(f"Book deletion failed: Book ID '{book_id}' not found.")
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    current_app.logger.info(f"Book ID '{book_id}' deleted successfully.")
    return jsonify({'message': 'Book deleted successfully'})


@books_bp.route('/books/details', methods=['GET'])
def get_book_details():
    """Fetch book details from the Google Books API."""
    current_app.logger.info("Attempting to fetch book details.")
    title = request.args.get('title')
    if not title:
        current_app.logger.warning("Book details retrieval failed: Missing title.")
        return jsonify({'error': 'Title is required'}), 400

    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params={'q': title})
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch book details from Google Books API: {e}")
        return jsonify({'error': 'Failed to fetch book details'}), 500

    data = response.json()
    if 'items' not in data or not data['items']:
        current_app.logger.warning(f"No book details found for title: {title}.")
        return jsonify({'error': 'No book details found'}), 404

    book_data = data['items'][0]['volumeInfo']
    current_app.logger.info(f"Book details fetched successfully for title: {title}.")
    return jsonify({
        'title': book_data.get('title'),
        'author': ', '.join(book_data.get('authors', [])),
        'published_date': book_data.get('publishedDate'),
        'summary': book_data.get('description'),
        'cover_image': book_data.get('imageLinks', {}).get('thumbnail')
    })
