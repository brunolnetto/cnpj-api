from unittest.mock import MagicMock

from backend.app.api.models.base import BatchModel
from backend.app.api.repositories.cnpj import CNPJRepository
from backend.app.api.services.cnpj import CNPJService

FOUND = "41286651000177"
MISSING = "11222333000181"
FORMATTED_MISSING = "11.222.333/0001-81"


def _service(records):
    repository = MagicMock()
    repository.get_cnpjs_info.return_value = records
    return CNPJService(repository)


def test_missing_cnpj_goes_to_fail_not_success():
    service = _service([{"cnpj_raw": FOUND, "nome": "ACME"}])

    result = service.get_cnpjs_info(BatchModel(batch=[FOUND, MISSING]))

    assert [record["cnpj_raw"] for record in result["success"]] == [FOUND]
    assert result["fail"] == {
        MISSING: {"is_valid": True, "reason": "CNPJ not found."}
    }


def test_invalid_and_missing_cnpjs_are_both_reported():
    service = _service({})

    result = service.get_cnpjs_info(BatchModel(batch=["123", MISSING]))

    assert result["success"] == []
    assert result["fail"]["123"]["is_valid"] is False
    assert result["fail"][MISSING] == {"is_valid": True, "reason": "CNPJ not found."}


def test_missing_cnpj_is_reported_by_the_string_sent():
    service = _service([])

    result = service.get_cnpjs_info(BatchModel(batch=[FORMATTED_MISSING]))

    assert list(result["fail"]) == [FORMATTED_MISSING]


def test_repository_does_not_build_records_for_missing_establishments(monkeypatch):
    from backend.app.api.models.cnpj import CNPJ

    repository = CNPJRepository(session=None)
    found = CNPJ("41286651", "0001", "77")
    missing = CNPJ("11222333", "0001", "81")

    # Only the found CNPJ has an establishment; partners and Simples have
    # defaults for every CNPJ
    monkeypatch.setattr(
        repository,
        "get_cnpjs_establishment",
        lambda cnpjs: {found.to_raw(): {"cnpj": "41.286.651/0001-77"}},
    )
    monkeypatch.setattr(repository, "get_cnpjs_company", lambda cnpjs: {})
    monkeypatch.setattr(repository, "get_cnpjs_partners", lambda cnpjs: {})
    monkeypatch.setattr(
        repository,
        "get_cnpjs_simples_simei",
        lambda cnpjs: {c.to_raw(): {"simples": {}, "simei": {}} for c in cnpjs},
    )

    records = repository.get_cnpjs_info([found, missing])

    assert [record["cnpj_raw"] for record in records] == [found.to_raw()]
