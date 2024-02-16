"""Test fixtures in conftest.py."""

from sqlalchemy import text


class TestFixtures:
    """Test fixtures in conftest.py."""

    def test_connection(self, connection):
        """Test connection fixture and test data."""
        result = connection.execute(text("SELECT * FROM user;"))
        assert result.fetchone() == (
            1,
            "john.doe",
            "johndoe@example.com",
            "yourSecurePassword",
        )

    def test_connection_insert(self, connection):
        """Test inserting data into the test database."""
        stmt = text(
            "INSERT INTO user (username, email, password) VALUES (:username, :email, :password);"
        )
        data = {
            "username": "john.smith",
            "email": "johnsmith@example.com",
            "password": "yourSecurePassword",
        }
        connection.execute(stmt, data)
        result = connection.execute(
            text("SELECT * FROM user WHERE username = 'john.smith';")
        )
        assert result.fetchone() is not None

    def test_connection_not_persists(self, connection):
        """Test that changes to the test database don't persist between tests.

        Note: relies on the previous test to insert data.
        """
        result = connection.execute(
            text("SELECT * FROM user WHERE username = 'john.smith';")
        )
        assert result.fetchone() is None
