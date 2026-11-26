"""
Response schemas must document the responses without changing them.

The payloads below are real responses captured from the sample database.
"""

import pytest
from fastapi.routing import APIRoute
from pydantic import TypeAdapter

from backend.app.api.app import app
from backend.app.api.models.responses import (
    Activities,
    CNPJBatchResult,
    CNPJRecord,
    CodeTextListing,
    Establishment,
    SimplesSimei,
)

ACTIVITY = {"code": "4321500", "text": "Instalação e manutenção elétrica"}

ESTABLISHMENT = {
    "abertura": "19/03/2021",
    "atividade_principal": {"code": "4120400", "text": "Construção de edifícios"},
    "atividades_secundarias": [ACTIVITY],
    "bairro": "Jardim Santa Lucia",
    "cep": "14.800-507",
    "cnpj": "41.286.651/0001-77",
    "complemento": "",
    "data_situacao": "19/03/2021",
    "data_situacao_especial": "",
    "email": "visao@araraquara.com.br",
    "fantasia": "",
    "logradouro": "Avenida Jose Cezarini",
    "motivo_situacao": "SEM MOTIVO",
    "municipio": "Araraquara",
    "numero": "883",
    "situacao": "ATIVA",
    "situacao_especial": "",
    "telefone": "(16) 3301-9200",
    "tipo": "MATRIZ",
    "uf": "SP",
}

SIMPLES_SIMEI = {
    "simei": {"data_exclusao": None, "data_opcao": None, "optante": False},
    "simples": {"data_exclusao": None, "data_opcao": "19/03/2021", "optante": True},
}

RECORD = {
    **ESTABLISHMENT,
    **SIMPLES_SIMEI,
    "capital_social": "100000.00",
    "cnpj_raw": "41286651000177",
    "efr": "",
    "natureza_juridica": "2062-Sociedade Empresária Limitada",
    "nome": "Rubinei Adriano De Souza Correa & Cia Ltda",
    "porte": "MICRO EMPRESA",
    "qsa": [
        {"nome": "RUBINEI ADRIANO DE SOUZA CORREA", "qual": "49-Sócio-Administrador"}
    ],
}

# What POST /cnpjs returns for a well-formed CNPJ missing from the database
STUB_RECORD = {"cnpj_raw": "11222333000181", "qsa": [], **SIMPLES_SIMEI}


def _roundtrip(model, payload):
    return TypeAdapter(model).dump_python(
        TypeAdapter(model).validate_python(payload), exclude_unset=True, mode="json"
    )


@pytest.mark.parametrize(
    "model, payload",
    [
        (CNPJRecord, RECORD),
        (CNPJRecord, STUB_RECORD),
        (Establishment, ESTABLISHMENT),
        (SimplesSimei, SIMPLES_SIMEI),
        # /activities returns the main activity code as an integer
        (
            Activities,
            {
                "atividade_principal": {"code": 4120400, "text": "x"},
                "atividades_secundarias": [ACTIVITY],
            },
        ),
        (
            CNPJBatchResult,
            {
                "success": [RECORD],
                "fail": {"123": {"is_valid": False, "reason": "Invalid length."}},
            },
        ),
        # Listings: paginated objects, or [code, object] pairs without pagination
        (CodeTextListing, [{"code": "111301", "text": "Cultivo de arroz"}]),
        (CodeTextListing, [["111301", {"code": "111301", "text": "Cultivo de arroz"}]]),
    ],
)
def test_schema_preserves_real_payload(model, payload):
    assert _roundtrip(model, payload) == payload


def test_unknown_fields_are_kept_not_dropped():
    payload = {**ESTABLISHMENT, "new_field": "value"}

    assert _roundtrip(Establishment, payload)["new_field"] == "value"


def test_every_api_route_documents_its_response():
    undocumented = [
        f"{sorted(route.methods)} {route.path}"
        for route in app.routes
        if isinstance(route, APIRoute)
        and route.path.startswith("/api/")
        and route.response_model is None
    ]

    assert undocumented == []
