from flask_sqlalchemy import SQLAlchemy
from models import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4), nullable=True)  # Year is a string
    status = db.Column(db.String(10), nullable=False, default='unread')  # "read" or "unread"
    cover_image = db.Column(db.String(2083), nullable=True)  # URL for the book cover
    summary = db.Column(db.Text, nullable=True)  # Summary of the book
    user_id = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<Book {self.id}: {self.title} by {self.author}>"