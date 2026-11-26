from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from backend.app.api.exceptions import not_found_handler


def _client() -> TestClient:
    app = FastAPI()
    app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)

    @app.get("/cnpj/{cnpj}")
    def get_cnpj(cnpj: str):
        raise HTTPException(status_code=404, detail=f"CNPJ {cnpj} not found.")

    return TestClient(app)


def test_endpoint_404_keeps_its_detail():
    response = _client().get("/cnpj/123")

    assert response.status_code == 404
    assert response.json() == {
        "error_code": "RESOURCE_NOT_FOUND",
        "detail": "CNPJ 123 not found.",
    }


def test_unknown_route_gets_generic_message():
    response = _client().get("/does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert body["error_code"] == "RESOURCE_NOT_FOUND"
    assert body["detail"] == "The requested resource could not be found."
    assert "suggestion" in body
