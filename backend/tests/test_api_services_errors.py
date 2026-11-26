from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from backend.app.api.exceptions import general_exception_handler
from backend.app.api.services.cnpj import CNPJService

VALID_CNPJ = "41286651000177"
INTERNAL_DETAIL = "connection to server at 10.0.0.5 failed"


def _service(side_effect) -> CNPJService:
    repository = MagicMock()
    repository.get_cnpjs_info.side_effect = side_effect
    return CNPJService(repository)


def test_invalid_input_is_a_400_with_its_message():
    service = _service(side_effect=None)

    with pytest.raises(HTTPException) as exc_info:
        service.get_cnpj_info("not-a-number")

    assert exc_info.value.status_code == 400
    assert "not a number" in exc_info.value.detail


def test_validation_error_from_repository_is_a_400():
    service = _service(side_effect=ValueError("Invalid CNPJ."))

    with pytest.raises(HTTPException) as exc_info:
        service.get_cnpj_info(VALID_CNPJ)

    assert exc_info.value.status_code == 400


def test_internal_error_is_not_turned_into_a_400():
    service = _service(side_effect=RuntimeError(INTERNAL_DETAIL))

    with pytest.raises(RuntimeError):
        service.get_cnpj_info(VALID_CNPJ)


def test_internal_error_reaches_client_as_generic_500():
    service = _service(side_effect=RuntimeError(INTERNAL_DETAIL))

    app = FastAPI()
    app.add_exception_handler(Exception, general_exception_handler)

    @app.get("/cnpj/{cnpj}")
    def get_cnpj(cnpj: str):
        return service.get_cnpj_info(cnpj)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get(f"/cnpj/{VALID_CNPJ}")

    assert response.status_code == 500
    assert response.json()["error_code"] == "INTERNAL_SERVER_ERROR"
    assert INTERNAL_DETAIL not in response.text
