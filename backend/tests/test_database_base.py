import pytest
from sqlalchemy.exc import (
    ArgumentError,
)

from backend.app.database.base import (
    Database,
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
