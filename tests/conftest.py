import pytest

@pytest.fixture(scope="session")
def test_client():
    from backend.api.app import app
    with app.test_client() as client:
        yield client
        

