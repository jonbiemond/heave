"""Universal test fixtures."""

import pytest
from sqlalchemy import create_engine, text


@pytest.fixture
def connection():
    """Create a new session for a test."""
    engine = create_engine("sqlite:///:memory:")

    # insert test data
    with open("tests/test_db.sql", "r") as f:
        statements = f.read().split(";")
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    yield engine.connect()
