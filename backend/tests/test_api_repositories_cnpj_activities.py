from contextlib import contextmanager

import pytest

from backend.app.api.models.cnpj import CNPJ
from backend.app.api.repositories import cnpj as cnpj_repository
from backend.app.api.repositories.cnpj import CNPJRepository


class RowsResult:
    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows


@pytest.fixture
def rows(monkeypatch):
    """Rows the activities query returns."""
    result_rows = []

    class Session:
        def execute(self, query, params=None):
            return RowsResult(result_rows)

    @contextmanager
    def fake_get_session(_db_name):
        yield Session()

    monkeypatch.setattr(cnpj_repository, "get_session", fake_get_session)
    return result_rows


@pytest.fixture
def repository():
    return CNPJRepository(session=None)


def test_activities_without_secondary_activities(repository, rows):
    rows.append(("41286648", "{'code': 4930201, 'text': 'Transporte'}", None))

    result = repository.get_cnpj_activities(CNPJ("41286648", "0001", "53"))

    assert result["atividade_principal"] == {"code": 4930201, "text": "Transporte"}
    assert result["atividades_secundarias"] == []


def test_activities_of_unknown_cnpj_is_empty(repository, rows):
    assert repository.get_cnpj_activities(CNPJ("11222333", "0001", "81")) == {}
