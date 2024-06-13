"""Test CLI."""

import os
from pathlib import Path
from unittest.mock import ANY, MagicMock, Mock

import pytest
from psycopg import OperationalError as PsycopgOperationalError
from sqlalchemy import Connection
from sqlalchemy.exc import OperationalError

from heave import Table, file
from heave.cli import cli, connect


class TestHelpers:
    """Test helper functions."""

    def test_connect(self):
        """Test connect returns a context with a session."""
        ctx = cli.make_context("test", ["TEST"])
        connect(ctx, "sqlite", database=":memory:")
        assert hasattr(ctx, "obj")
        assert isinstance(ctx.obj, Connection)

    def test_connect_invalid_database(self, monkeypatch):
        """Test connect exits if database connection fails."""
        # mock engine
        engine = Mock()
        engine.connect.side_effect = Exception
        monkeypatch.setattr("heave.cli.create_engine", Mock(return_value=engine))
        ctx = cli.make_context("test", ["TEST"])
        with pytest.raises(SystemExit):
            connect(ctx, "sqlite", database=":memory:")

    def test_connect_invalid_password(self, monkeypatch):
        """Connect prompts for password if connection fails."""
        # mock engine
        mock_engine = Mock()
        mock_engine.connect.side_effect = OperationalError(
            statement="",
            orig=PsycopgOperationalError(
                "connection failed: fe_sendauth: no password supplied"
            ),
            params={},
        )
        monkeypatch.setattr("heave.cli.create_engine", Mock(return_value=mock_engine))
        # mock prompt
        mock_prompt = Mock(return_value="test")
        monkeypatch.setattr("click.prompt", mock_prompt)
        ctx = cli.make_context("test", ["TEST"])
        with pytest.raises(SystemExit):
            connect(ctx, "sqlite", database=":memory:", user="test")
        assert mock_prompt.called

    def test_echo(self, monkeypatch):
        """Connect passes the echo value to create_engine."""
        mock_create_engine = MagicMock()
        monkeypatch.setattr("heave.cli.create_engine", mock_create_engine)
        connect(
            cli.make_context("test", ["TEST"]),
            "sqlite",
            database=":memory",
            user="test",
            echo=True,
        )
        assert mock_create_engine.call_args.kwargs["echo"] is True


class TestCli:
    """Test the CLI."""

    test_file = "temp.csv"

    @pytest.fixture(autouse=True)
    def temp_file(self):
        """Create a temporary csv file."""
        with open(self.test_file, "w") as f:
            f.write("header1,header2\n")
            f.write("data1,data2\n")
        yield
        os.remove(self.test_file)

    def test_help(self, runner, monkeypatch):
        """Connect is not called if the help flag is passed."""
        mock_connect = Mock()
        monkeypatch.setattr("heave.cli.connect", mock_connect)
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert mock_connect.called is False
        assert "Show this message and exit." in result.output

    def test_connection(self, runner, monkeypatch):
        """Connect is called with defaults if no connection parameters are supplied."""
        mock_connect = Mock()
        monkeypatch.setattr("heave.cli.connect", mock_connect)
        monkeypatch.delenv("PGHOST", raising=False)
        monkeypatch.delenv("PGPORT", raising=False)
        monkeypatch.delenv("PGUSER", raising=False)
        monkeypatch.delenv("PGDATABASE", raising=False)
        runner.invoke(cli, ["insert"])
        mock_connect.assert_called_with(
            ANY,
            "postgresql",
            "postgres",
            "localhost",
            "5432",
            "",
            "psycopg",
            echo=False,
        )

    def test_connection_envvars(self, runner, monkeypatch):
        """Connect is called with values from environment variables if they exist and no connection parameters are supplied."""
        mock_connect = Mock()
        monkeypatch.setattr("heave.cli.connect", mock_connect)
        monkeypatch.setenv("PGHOST", "myhost")
        monkeypatch.setenv("PGPORT", "1234")
        monkeypatch.setenv("PGUSER", "myuser")
        monkeypatch.setenv("PGDATABASE", "mydb")
        runner.invoke(cli, ["insert"])
        mock_connect.assert_called_with(
            ANY, "postgresql", "mydb", "myhost", "1234", "myuser", "psycopg", echo=False
        )

    def test_echo(self, runner, monkeypatch):
        """Connect is called with echo=True if the echo flag is passed."""
        mock_connect = Mock()
        monkeypatch.setattr("heave.cli.connect", mock_connect)
        runner.invoke(cli, ["--echo", "insert"])
        assert mock_connect.call_args.kwargs["echo"] is True

    def test_insert(self, runner, monkeypatch):
        """Test the insert command."""
        data = Table(
            [
                ("username", "email", "password"),
                ("jane.doe", "janedoe@example.com", "yourSecurePassword"),
            ]
        )
        monkeypatch.setattr("heave.file.read_csv", Mock(return_value=data))
        result = runner.invoke(cli, ["insert", "--table", "user", self.test_file])
        assert result.exit_code == 0
        assert "Inserted rows into user." in result.output

    def test_insert_schema(self, runner, monkeypatch):
        """Schema option is passed to table reflection."""
        mock_reflect_table = Mock()
        monkeypatch.setattr("heave.sql.reflect_table", mock_reflect_table)
        runner.invoke(
            cli, ["insert", "--schema", "sales", "--table", "record", self.test_file]
        )
        mock_reflect_table.assert_called_with(ANY, "record", "sales")

    def test_insert_error(self, runner, monkeypatch):
        """Changes are rolled back on error."""
        # insert duplicate data
        data = Table(
            [
                ("username", "email", "password"),
                ("jane.doe", "janedoe@example.com", "yourSecurePassword"),
                ("jane.doe", "janedoe@example.com", "yourSecurePassword"),
            ]
        )
        monkeypatch.setattr("heave.file.read_csv", Mock(return_value=data))
        result = runner.invoke(cli, ["insert", "--table", "user", self.test_file])
        assert result.exit_code == 1
        result = runner.invoke(cli, ["read", "--table", "user", self.test_file])
        assert result.exit_code == 0
        table = file.read_csv(Path(self.test_file))
        for row in table.rows:
            assert row[1] != "jane.doe"

    def test_insert_conflict(self, runner, monkeypatch):
        """The on-conflict option is passed to the insert function."""
        mock_insert = Mock()
        monkeypatch.setattr("heave.sql.insert", mock_insert)
        result = runner.invoke(
            cli,
            ["insert", "--table", "user", "--on-conflict", "nothing", self.test_file],
        )
        assert result.exit_code == 0
        mock_insert.assert_called()
        assert mock_insert.call_args.kwargs["on_conflict"] == "nothing"

    def test_insert_conflict_invalid(self, runner):
        """The on-conflict option only accepts valid choices."""
        result = runner.invoke(
            cli, ["insert", "--table", "user", "--on-conflict", "foo", self.test_file]
        )
        assert result.exit_code == 2
        assert (
            "Error: Invalid value for '-oc' / '--on-conflict': 'foo' is not one of 'nothing', 'update'."
            in result.output
        )

    def test_read(self, runner, monkeypatch):
        """write_csv is called from the read command."""
        mock_write_csv = Mock()
        monkeypatch.setattr("heave.file.write_csv", mock_write_csv)
        result = runner.invoke(cli, ["read", "--table", "user", self.test_file])
        assert mock_write_csv.called
        assert result.exit_code == 0
        assert f"Wrote data to {self.test_file}." in result.output

    def test_read_schema(self, runner, monkeypatch):
        """The schema option is passed to table reflection."""
        mock_reflect_table = Mock()
        monkeypatch.setattr("heave.sql.reflect_table", mock_reflect_table)
        runner.invoke(
            cli, ["read", "--schema", "sales", "--table", "record", self.test_file]
        )
        mock_reflect_table.assert_called_with(ANY, "record", "sales")

    def test_read_invalid_directory(self, runner):
        """A Click error is raised for a non-existant directory."""
        result = runner.invoke(cli, ["read", "--table", "user", "invalid/myfile.csv"])
        assert result.exit_code == 1
        assert "Error: No such directory: 'invalid'" in result.output
