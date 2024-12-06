from app import db
from utils.hash_utils import generate_salt, hash_password

class User(db.Model):
    """User model for the database.

    Attributes:
        id (int): The unique identifier for a user.
        username (str): The unique username for the user.
        salt (str): The salt used for hashing the user's password.
        hashed_password (str): The hashed password of the user.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, salt, hashed_password):
        """Initializes a new user.

        Args:
            username (str): The username of the user.
            salt (str): The salt used for password hashing.
            hashed_password (str): The hashed password.
        """
        self.username = username
        self.salt = salt
        self.hashed_password = hashed_password

def create_user(username, password):
    """Creates a new user in the database.

    Args:
        username (str): The username of the new user.
        password (str): The password for the new user.

    Returns:
        tuple: A boolean indicating success, and a message string.
    """
    try:
        salt = generate_salt()
        hashed_password = hash_password(password, salt)
        user = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(user)  # Use db.session to manage transactions
        db.session.commit()
        return True, "User created successfully"
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def get_user_by_username(username):
    """Fetches a user by their username.

    Args:
        username (str): The username to search for.

    Returns:
        User: The user object if found, or None if not.
    """
    return User.query.filter_by(username=username).first()

def update_user_password(username, new_password):
    """Updates the password for a specified user.

    Args:
        username (str): The username of the user.
        new_password (str): The new password.

    Returns:
        tuple: A boolean indicating success, and a message string.
    """
    user = get_user_by_username(username)
    if user:
        try:
            user.salt = generate_salt()
            user.hashed_password = hash_password(new_password, user.salt)
            db.session.commit()
            return True, "Password updated successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    return False, "User not found"
