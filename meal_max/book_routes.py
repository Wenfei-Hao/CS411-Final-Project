from flask import Blueprint, request, jsonify
import requests
from models.book_model import Book, db

books_bp = Blueprint('books', __name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


@books_bp.route('/health', methods=['GET'])
def health():
    """Health check route to confirm the app is running."""
    return jsonify({'status': 'App is running'}), 200


@books_bp.route('/books', methods=['POST'])
def add_book():
    """Add a new book to the database."""
    data = request.json
    title = data.get('title')
    author = data.get('author')
    year = data.get('year', '')

    if not title or not author:
        return jsonify({'error': 'Title and Author are required'}), 400

    book = Book(title=title, author=author, year=year)
    db.session.add(book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully', 'book_id': book.id}), 201


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieve a book by its ID."""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

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
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    status = data.get('status')
    if status not in ['read', 'unread']:
        return jsonify({'error': 'Invalid status. Use "read" or "unread".'}), 400

    book.status = status
    db.session.commit()

    return jsonify({'message': 'Reading status updated'})


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the database."""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'})


@books_bp.route('/books/details', methods=['GET'])
def get_book_details():
    """Fetch book details from the Google Books API."""
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    response = requests.get(GOOGLE_BOOKS_API_URL, params={'q': title})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch book details'}), 500

    data = response.json()
    if 'items' not in data or not data['items']:
        return jsonify({'error': 'No book details found'}), 404

    book_data = data['items'][0]['volumeInfo']
    return jsonify({
        'title': book_data.get('title'),
        'author': ', '.join(book_data.get('authors', [])),
        'published_date': book_data.get('publishedDate'),
        'summary': book_data.get('description'),
        'cover_image': book_data.get('imageLinks', {}).get('thumbnail')
    })
