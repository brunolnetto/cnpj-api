import pytest
from unittest import mock


@pytest.fixture(scope="session")
def test_client():
    from backend.app.api.app import app

    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_logging(mocker):
    """Provides a mock object for the logging module."""
    return mocker.patch("backend.setup.logging.logger.error")


@pytest.fixture
def mock_create_engine():
    with mock.patch("sqlalchemy.create_engine") as mock_engine:
        yield mock_engine


@pytest.fixture
def mock_sessionmaker():
    with mock.patch("sqlalchemy.orm.sessionmaker") as mock_session:
        yield mock_session
