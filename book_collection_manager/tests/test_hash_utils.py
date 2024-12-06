import unittest
from utils.hash_utils import generate_salt, hash_password, verify_password

class TestHashUtils(unittest.TestCase):
    """Unit tests for hash_utils.py."""

    def test_generate_salt(self):
        """Test that generate_salt produces unique salts."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        self.assertNotEqual(salt1, salt2, "generate_salt should produce unique values")

    def test_hash_password(self):
        """Test that hash_password produces a consistent hash for the same inputs."""
        password = "mypassword"
        salt = "randomsalt"
        hashed1 = hash_password(password, salt)
        hashed2 = hash_password(password, salt)
        self.assertEqual(hashed1, hashed2, "hash_password should produce the same hash for identical inputs")

    def test_verify_password(self):
        """Test that verify_password correctly verifies the password."""
        password = "mypassword"
        salt = generate_salt()
        hashed_password = hash_password(password, salt)
        self.assertTrue(verify_password(password, salt, hashed_password), "verify_password should return True for correct password")
        self.assertFalse(verify_password("wrongpassword", salt, hashed_password), "verify_password should return False for incorrect password")

if __name__ == "__main__":
    unittest.main()
