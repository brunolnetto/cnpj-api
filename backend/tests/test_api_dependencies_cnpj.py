from contextlib import contextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.dependencies import cnpj as cnpj_dependencies
from backend.app.api.repositories.cnpj import CNPJRepository


class FakeSession:
    def __init__(self):
        self.closed = False


def test_repository_session_lives_for_the_whole_request(monkeypatch):
    session = FakeSession()

    @contextmanager
    def fake_get_session(_db_name):
        try:
            yield session
        finally:
            session.closed = True

    monkeypatch.setattr(cnpj_dependencies, "get_session", fake_get_session)

    app = FastAPI()

    @app.get("/check")
    def check(
        repository: CNPJRepository = cnpj_dependencies.CNPJRepositoryDependency,
    ):
        return {"closed_during_request": repository.session.closed}

    response = TestClient(app).get("/check")

    assert response.json() == {"closed_during_request": False}
    assert session.closed is True
