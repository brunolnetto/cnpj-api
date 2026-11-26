"""
Searches without matches must answer 200 with an empty value of the
documented type, never a 500 from response validation.
"""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from backend.app.api.app import app
from backend.app.api.dependencies.auth import jwt_bearer
from backend.app.api.services.cnpj import CNPJService, get_cnpj_service

MISSING_CNPJ = "11222333000181"


@pytest.fixture
def client():
    repository = MagicMock()
    # What the repository answers when it finds nothing
    repository.get_cnpjs_raw.return_value = []
    repository.get_cnpjs_info.return_value = {}
    repository.get_cnpjs_company.return_value = {}

    app.dependency_overrides[jwt_bearer] = lambda: {"sub": "test"}
    app.dependency_overrides[get_cnpj_service] = lambda: CNPJService(repository)
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides.clear()


def test_cnpj_search_without_matches_is_empty_list(client):
    response = client.get("/api/cnpjs")

    assert response.status_code == 200
    assert response.json() == []


def test_batch_with_only_invalid_cnpjs(client):
    response = client.post("/api/cnpjs", json={"batch": ["123"]})

    assert response.status_code == 200
    assert response.json()["success"] == []
    assert response.json()["fail"]["123"]["is_valid"] is False


def test_company_batch_without_matches_is_empty_dict(client):
    response = client.post("/api/cnpjs/company", json={"batch": [MISSING_CNPJ]})

    assert response.status_code == 200
    assert response.json() == {}
