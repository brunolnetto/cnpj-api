from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from backend.app.api.models.base import BatchModel
from backend.app.api.models.misc import PaginatedLimitOffsetParams
from backend.app.api.services.cnpj import CNPJService

VALID_CNPJ = "41286651000177"


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def service(repository):
    return CNPJService(repository)


def _assert_404(call):
    with pytest.raises(HTTPException) as exc_info:
        call()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail


def test_unknown_cnpj_is_404(service, repository):
    repository.get_cnpjs_info.return_value = {}

    _assert_404(lambda: service.get_cnpj_info(VALID_CNPJ))


def test_unknown_cnpj_company_is_404(service, repository):
    repository.get_cnpjs_company.return_value = {}

    _assert_404(lambda: service.get_cnpj_company(VALID_CNPJ))


def test_cnpj_without_partners_is_404(service, repository):
    repository.get_cnpjs_partners.return_value = {}

    _assert_404(lambda: service.get_cnpj_partners(VALID_CNPJ))


def test_unknown_city_is_404(service, repository):
    repository.get_city.return_value = {}

    _assert_404(lambda: service.get_city("999999"))


def test_unknown_cnae_is_404(service, repository):
    repository.get_cnae_list.return_value = []

    _assert_404(lambda: service.get_cnae_description("1"))


def test_states_search_without_results_is_empty_list(service, repository):
    # The repository answers {} when there are no CNPJs
    repository.get_cnpjs_by_states.return_value = {}

    result = service.get_cnpjs_by_states(BatchModel(batch=["SP"]), limit=10, offset=0)

    assert result == []


def test_cnaes_search_without_results_is_empty_list(service, repository):
    repository.get_cnpjs_by_cnaes.return_value = {}

    result = service.get_cnpjs_by_cnaes(
        BatchModel(batch=["4781400"]), PaginatedLimitOffsetParams()
    )

    assert result == []


def test_batch_lookup_without_matches_is_empty_list(service, repository):
    repository.get_cities_list.return_value = []

    assert service.get_cities_list(BatchModel(batch=["1"])) == []


def test_repository_cnpjs_info_with_no_cnpjs_does_not_query():
    from backend.app.api.repositories.cnpj import CNPJRepository

    session = MagicMock()

    assert CNPJRepository(session).get_cnpjs_info([]) == {}
    session.execute.assert_not_called()
