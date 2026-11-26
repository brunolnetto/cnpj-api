"""
User input must reach the database only as bound parameters, never as SQL text.
"""

import pytest

from backend.app.api.models.cnpj import CNPJQueryParams
from backend.app.api.models.misc import PaginatedLimitOffsetParams
from backend.app.api.repositories.cnpj import CNPJRepository

PAYLOAD = "1' or '1'='1"


class EmptyResult:
    def fetchall(self):
        return []


class RecordingSession:
    def __init__(self):
        self.calls = []

    def execute(self, query, params=None):
        self.calls.append((str(query), params or {}))
        return EmptyResult()


@pytest.fixture
def session():
    return RecordingSession()


@pytest.fixture
def repository(session, monkeypatch):
    repository = CNPJRepository(session)
    monkeypatch.setattr(repository, "get_cnpjs_info", lambda cnpj_list: {})
    return repository


def _single_call(session):
    assert len(session.calls) == 1
    return session.calls[0]


def test_cnpjs_filters_are_bound(repository, session):
    query_params = CNPJQueryParams(
        city_name="7107",
        state_abbrev="SP",
        zipcode="14800507",
        cnae_code="4321500",
        activity_start_date="2021-03-19",
        limit=20,
        offset=5,
    )
    # Set after validation so this test does not depend on the validator fix in #209
    query_params.state_abbrev = "SP"

    repository.get_cnpjs_raw(query_params)

    sql, params = _single_call(session)
    for value in ("7107", "14800507", "4321500", "20210319"):
        assert value not in sql
    assert params["city"] == "7107"
    assert params["state"] == "SP"
    assert params["zipcode"] == "14800507"
    assert params["cnae_code"] == "4321500"
    assert params["cnae_code_int"] == 4321500
    assert params["start_date"] == "20210319"
    assert (params["limit"], params["offset"]) == (20, 5)


def test_cnpjs_without_filters_binds_only_pagination(repository, session):
    repository.get_cnpjs_raw(CNPJQueryParams())

    _, params = _single_call(session)
    assert set(params) == {"limit", "offset"}


def test_city_lookup_is_bound(repository, session):
    repository.city_exists(PAYLOAD)

    sql, params = _single_call(session)
    assert PAYLOAD not in sql
    assert params == {"city_name": PAYLOAD}


def test_cnpjs_with_cnae_is_bound(repository, session):
    repository.get_cnpjs_with_cnae(PAYLOAD, limit=5, offset=0)

    sql, params = _single_call(session)
    assert PAYLOAD not in sql
    assert params["cnae_code"] == PAYLOAD
    assert params["cnae_pattern"] == f"%{PAYLOAD}%"


def test_cnpjs_by_cnaes_is_bound(repository, session):
    repository.get_cnpjs_by_cnaes(
        ["4781400", PAYLOAD], PaginatedLimitOffsetParams(limit=5)
    )

    sql, params = _single_call(session)
    assert PAYLOAD not in sql
    assert "4781400" not in sql
    assert params["cnaes"] == ["4781400", PAYLOAD]
    assert params["cnae_pattern_1"] == f"%{PAYLOAD}%"


def test_cnpjs_by_states_is_bound(repository, session):
    repository.get_cnpjs_by_states(["SP", PAYLOAD], limit=5, offset=0)

    sql, params = _single_call(session)
    assert PAYLOAD not in sql
    assert params["states"] == ["SP", PAYLOAD]


def test_zipcode_with_leading_zero_is_bound_unchanged(repository, session):
    repository.get_cnpjs_raw(CNPJQueryParams(zipcode="09857010"))

    _, params = _single_call(session)
    assert params["zipcode"] == "09857010"
