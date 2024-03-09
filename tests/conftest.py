"""Universal test fixtures."""

import pytest
from click.testing import CliRunner
from sqlalchemy import Connection, Engine, create_engine, text

ENV = {"TESTING": "True"}


def init_db() -> Engine:
    """Initialize a new SQLite database and load with test data."""
    engine = create_engine("sqlite:///:memory:")

    # insert test data
    with open("tests/test_db.sql") as f:
        statements = f.read().split(";")
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    return engine


@pytest.fixture(scope="function")
def connection() -> Connection:
    """Open a connection to the test database."""
    engine = init_db()

    yield engine.connect()


@pytest.fixture(scope="function")
def runner(monkeypatch) -> CliRunner:
    """Click test runner."""
    engine = init_db()

    def patch_connect(context, *args, **kwargs):
        context.obj = context.with_resource(engine.begin())

    monkeypatch.setattr("heave.cli.connect", patch_connect)

    return CliRunner(env=ENV)
