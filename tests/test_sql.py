"""Tests for the sql module."""

from unittest.mock import Mock

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from heave import Table, sql
from heave.sql import InvalidDb, update_from_conflict


class TestSql:
    """Test sql functions."""

    def test_reflect_table(self, connection):
        """Test the reflect_table function."""
        table = sql.reflect_table(connection, "user")
        assert table.name == "user"
        table = sql.reflect_table(connection, "record", "sales")
        assert table.name == "record"
        assert table.schema == "sales"

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

    def test_insert_conflict_nothing(self, connection):
        """Test that insert handles skips conflicts."""
        data = Table(
            [
                ("username", "email", "password"),
                ("jane.doe", "janedoe@example.com", "yourSecurePassword"),
                ("john.doe", "johndoe@example.com", "yourSecurePassword"),
            ]
        )
        sql_table = sql.reflect_table(connection, "user")
        sql.insert(connection, sql_table, data, on_conflict="nothing")
        result = connection.execute(
            text("SELECT password FROM user WHERE username = 'john.doe';")
        )
        assert result.scalar() == "yourSecurePassword"
        result = connection.execute(
            text("SELECT * FROM user WHERE username = 'jane.doe';")
        )
        assert result.fetchone() is not None

    def test_insert_conflict_update_invalid_db(self, connection):
        """Test that insert raises an Invalid DB error when called with update on conflict."""
        data = Table(
            [
                ("username", "email", "password"),
                ("john.doe", "johndoe@example.com", "yourSecurePassword"),
            ]
        )
        sql_table = sql.reflect_table(connection, "user")

        with pytest.raises(InvalidDb):
            sql.insert(connection, sql_table, data, on_conflict="update")

    def test_update_from_conflict(self, connection, monkeypatch):
        """Test that update_from_conflict writes the correct SQL."""
        mock_orig = Mock()
        mock_orig.diag.constraint_name = "uq_username"
        mock_integrity_error = IntegrityError("", {}, orig=mock_orig)
        data = Table(
            [
                ("username", "email", "password"),
                ("john.doe", "johndoe@example.com", "yourSecurePassword"),
            ]
        )
        sql_table = sql.reflect_table(connection, "user")
        uq_constraint = next(
            cns
            for cns in sql_table.constraints
            if "username" in [col.name for col in cns.columns]
        )
        uq_constraint.name = mock_orig.diag.constraint_name
        sql_table.constraints = [uq_constraint]
        stmt = update_from_conflict(
            sql_table, mock_integrity_error, data.header, next(data.rows)
        )
        assert (
            str(stmt)
            == 'UPDATE "user" SET email=:email, password=:password WHERE "user".username = :username_1'
        )

    def test_read(self, connection):
        """Test the read function."""
        data = sql.read(connection, sql.reflect_table(connection, "user"))
        assert data == Table(
            [
                ("id", "username", "email", "password"),
                (1, "john.doe", "johndoe@example.com", "yourSecurePassword"),
                (2, "jane.smith", "janesmith@example.com", "anotherSecurePassword"),
                (3, "bob.johnson", "bob.johnson@example.com", "superSecurePassword"),
            ]
        )
