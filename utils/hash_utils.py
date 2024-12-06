import hashlib
import os

def generate_salt():
    """Generates a random salt value.

    Returns:
        str: A randomly generated salt value as a hexadecimal string.
    """
    return os.urandom(16).hex()

def hash_password(password, salt):
    """Generates a hash for the given password and salt.

    Args:
        password (str): The plain-text password.
        salt (str): The salt value.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password, salt, hashed_password):
    """Verifies if the given password matches the stored hashed password.

    Args:
        password (str): The plain-text password.
        salt (str): The salt value.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return hash_password(password, salt) == hashed_password
