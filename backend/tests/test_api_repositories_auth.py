import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.api.repositories.auth import ApiClientRepository
from backend.app.database.models.auth import ApiClient
from backend.app.utils.security import (
    generate_client_credentials,
    hash_client_secret,
    verify_client_secret,
)


@pytest.fixture
def repository():
    engine = create_engine("sqlite://")
    ApiClient.__table__.create(engine)
    session = sessionmaker(bind=engine)()

    yield ApiClientRepository(session)

    session.close()
    engine.dispose()


def test_generated_credentials_are_unique():
    first = generate_client_credentials()
    second = generate_client_credentials()

    assert first[0] != second[0]
    assert first[1] != second[1]
    assert first[0].startswith("cli_")


def test_secret_hash_verification():
    secret_hash = hash_client_secret("s3cret")

    assert secret_hash != "s3cret"
    assert verify_client_secret("s3cret", secret_hash)
    assert not verify_client_secret("wrong", secret_hash)


def test_created_client_stores_only_the_hash(repository):
    client, client_secret = repository.create("Acme")

    assert client.apcl_secret_hash != client_secret
    assert client.apcl_is_active


def test_authenticate_with_valid_credentials(repository):
    client, client_secret = repository.create("Acme")

    authenticated = repository.authenticate(client.apcl_client_id, client_secret)

    assert authenticated is not None
    assert authenticated.apcl_client_id == client.apcl_client_id


def test_authenticate_rejects_wrong_secret(repository):
    client, _ = repository.create("Acme")

    assert repository.authenticate(client.apcl_client_id, "wrong") is None


def test_authenticate_rejects_unknown_client(repository):
    assert repository.authenticate("cli_unknown", "whatever") is None


def test_deactivated_client_cannot_authenticate(repository):
    client, client_secret = repository.create("Acme")

    assert repository.set_active(client.apcl_client_id, False)

    assert repository.authenticate(client.apcl_client_id, client_secret) is None
    assert not repository.is_active(client.apcl_client_id)


def test_set_active_on_unknown_client(repository):
    assert repository.set_active("cli_unknown", False) is False
