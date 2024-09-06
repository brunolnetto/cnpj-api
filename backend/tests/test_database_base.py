import pytest
from unittest.mock import patch
from sqlalchemy.exc import (
    ArgumentError,
)

from backend.app.database.base import (
    MultiDatabase, Database,
)

@pytest.fixture
def mock_create_engine(mocker):
    """Provides a mock object for the create_engine function."""
    return mocker.patch("sqlalchemy.create_engine")


@pytest.fixture
def mock_sessionmaker(mocker):
    """Provides a mock object for the sessionmaker function."""
    return mocker.patch("sqlalchemy.orm.sessionmaker")


def test_database_init_invalid_uri(mocker):
    """Tests Database object initialization with an invalid URI (raises exception)."""
    mock_uri = "invalid_uri"
    with pytest.raises(ArgumentError):
        Database(mock_uri)


def test_test_connection_error(mocker):
    """Tests the test_connection method with a connection error (raises exception)."""
    mock_uri = "postgresql://user:password@host:1234/database"
    db = Database(mock_uri)

    # Mock a failing connection (don't patch connect method directly)
    error = Exception("Test Error")
    mocker.patch.object(db.engine, "connect", side_effect=error)
    with pytest.raises(Exception):
        db.test_connection()

