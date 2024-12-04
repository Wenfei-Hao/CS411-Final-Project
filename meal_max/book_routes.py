from flask import Blueprint, request, jsonify
import requests
from models.book_model import Book, db

books_bp = Blueprint('books', __name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

