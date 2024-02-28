"""Tests for the sql module."""
from sqlalchemy import text

from heave import Table, sql


class TestSql:
    """Test sql functions."""

    def test_reflect_table(self, connection):
        """Test the reflect_table function."""
        table = sql.reflect_table(connection, "user")
        assert table.name == "user"

    def test_insert(self, connection):
        """Test the insert function."""
        data = Table(
            [
                ("username", "email", "password"),
                ("jane.doe", "janedoe@example.com", "yourSecurePassword"),
            ]
        )
        sql_table = sql.reflect_table(connection, "user")
        sql.insert(connection, sql_table, data)
        result = connection.execute(
            text("SELECT * FROM user WHERE username = 'jane.doe';")
        )
        assert result.fetchone() is not None
