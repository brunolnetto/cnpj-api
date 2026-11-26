from typing import Dict, List, Union

from fastapi import APIRouter, Request, Depends

from backend.app.api.services.cnpj import CNPJService, CNPJServiceDependency
from backend.app.api.rate_limiter import rate_limit
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.api.models.base import BatchModel
from backend.app.api.models.cnpj import CNPJBatch, CNPJQueryParams
from backend.app.api.models.misc import LimitOffsetParams, PaginatedLimitOffsetParams
from backend.app.api.models.responses import (
    Activities,
    CityCandidates,
    CNPJBatchResult,
    CNPJRecord,
    CodeDescriptionMap,
    CodeText,
    CodeTextListing,
    Company,
    Establishment,
    Partners,
    SimplesSimei,
)

# Types
CodeType = Union[str, int]

router = APIRouter(tags=["CNPJ"], dependencies=[JWTDependency])


@router.get(
    "/cnaes",
    response_model=CodeTextListing,
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnaes(
    request: Request,
    query_params: PaginatedLimitOffsetParams = Depends(),
    search_token: str = "",
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List CNAEs, paginated. With `search_token`, return the CNAEs whose
    description contains the token instead.
    """
    return (
        cnpj_service.get_cnae_by_token(search_token)
        if search_token != ""
        else cnpj_service.get_cnaes(query_params)
    )


@router.post(
    "/cnaes",
    response_model=List[CodeText],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnae_objects(
    request: Request,
    cnae_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the CNAEs for a batch of codes. Unknown codes are left out; an empty
    list means none was found.
    """
    return cnpj_service.get_cnae_objects(cnae_code_batch)


@router.post(
    "/cnaes/cnpjs",
    response_model=List[CNPJRecord],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_by_cnaes(
    request: Request,
    cnae_batch: BatchModel,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List active establishments whose main or secondary CNAE is in the batch,
    paginated with `limit` and `offset`.
    """
    return cnpj_service.get_cnpjs_by_cnaes(cnae_batch, query_params)


@router.get(
    "/cnaes/{cnae_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnae/{cnae_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnae_description(
    request: Request,
    cnae_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a CNAE by code. Responds 404 if it does not exist.
    """
    return cnpj_service.get_cnae_description(cnae_code)


@router.get(
    "/cnaes/{cnae_code}/cnpjs",
    response_model=List[CNPJRecord],
    response_model_exclude_unset=True,
)
@router.get(
    "/cnae/{cnae_code}/cnpjs",
    response_model=List[CNPJRecord],
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpjs_with_cnae(
    request: Request,
    cnae_code: CodeType,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List active establishments whose main or secondary CNAE is `cnae_code`,
    paginated with `limit` and `offset`.
    """
    return cnpj_service.get_cnpjs_with_cnae(cnae_code, query_params)


@router.post(
    "/states/cnpjs",
    response_model=List[CNPJRecord],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_by_state(
    request: Request,
    state_batch: BatchModel,
    query_params: LimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List active establishments in the states of the batch (e.g. `["SP", "RJ"]`),
    paginated with `limit` and `offset`.
    """
    return cnpj_service.get_cnpjs_by_states(
        state_batch, query_params.limit, query_params.offset
    )


@router.get(
    "/company/sizes",
    response_model=CodeDescriptionMap,
    response_model_exclude_unset=True,
)
@rate_limit()
def get_company_sizes(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the company size codes and their descriptions.
    """
    return cnpj_service.get_company_size_dict()


@router.get(
    "/company/situations",
    response_model=CodeDescriptionMap,
    response_model_exclude_unset=True,
)
@router.get(
    "/company/situation",
    response_model=CodeDescriptionMap,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_situations(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the company registration situation codes and their descriptions.
    """
    return cnpj_service.get_company_situation_dict()


@router.get(
    "/establishment/types",
    response_model=CodeDescriptionMap,
    response_model_exclude_unset=True,
)
@rate_limit()
def get_establishment_sizes(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the establishment type codes (headquarters or branch) and their
    descriptions.
    """
    return cnpj_service.get_establishment_type_dict()


@router.get(
    "/cities/{city_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
)
@router.get(
    "/city/{city_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_city(
    request: Request,
    city_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a city by code. Responds 404 if it does not exist.
    """
    return cnpj_service.get_city(city_code)


@router.get(
    "/cities",
    response_model=List[CodeText],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cities(
    request: Request,
    query_params: LimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List cities, paginated with `limit` and `offset`.
    """
    return cnpj_service.get_cities(query_params.limit, query_params.offset)


@router.post(
    "/cities",
    response_model=List[CodeText],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cities_list(
    request: Request,
    cities_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the cities for a batch of codes. Unknown codes are left out.
    """
    return cnpj_service.get_cities_list(cities_code_batch)


@router.post(
    "/cities/infer",
    response_model=CityCandidates,
    response_model_exclude_unset=True,
)
@rate_limit()
def infer_city(
    request: Request,
    city_name_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    For each city name in the batch, return the most similar city names
    known to the API (useful for misspelled or unaccented names).
    """
    return cnpj_service.get_city_candidates(city_name_batch)


@router.get(
    "/legal-natures/{legal_nature_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
)
@router.get(
    "/legal-nature/{legal_nature_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_legal_nature(
    request: Request,
    legal_nature_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a legal nature by code. Responds 404 if it does not exist.
    """
    return cnpj_service.get_legal_nature(legal_nature_code)


@router.get(
    "/legal-natures",
    response_model=CodeTextListing,
    response_model_exclude_unset=True,
)
@rate_limit()
def get_legal_natures(
    request: Request,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List legal natures, paginated.
    """
    return cnpj_service.get_legal_natures(query_params)


@router.post(
    "/legal-natures",
    response_model=List[CodeText],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_legal_natures_list(
    request: Request,
    legal_natures_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the legal natures for a batch of codes. Unknown codes are left out.
    """
    return cnpj_service.get_legal_natures_list(legal_natures_code_batch)


@router.get(
    "/registration-statuses/{registration_status_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
)
@router.get(
    "/registration-status/{registration_status_code}",
    response_model=CodeText,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_registration_status(
    request: Request,
    registration_status_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a registration status by code. Responds 404 if it does not exist.
    """
    return cnpj_service.get_registration_status(registration_status_code)


@router.get(
    "/registration-statuses",
    response_model=CodeTextListing,
    response_model_exclude_unset=True,
)
@rate_limit()
def get_registration_statuses(
    request: Request,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List registration statuses, paginated.
    """
    return cnpj_service.get_registration_statuses(query_params)


@router.post(
    "/registration-statuses",
    response_model=List[CodeText],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_registration_statuses_list(
    request: Request,
    registration_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the registration statuses for a batch of codes. Unknown codes are
    left out.
    """
    return cnpj_service.get_registration_statuses_list(registration_code_batch)


@router.get(
    "/cnpjs/{cnpj}",
    response_model=CNPJRecord,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}",
    response_model=CNPJRecord,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_info(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the full record of a CNPJ (14 digits): establishment, company,
    partners and Simples/SIMEI. Responds 404 if it does not exist.
    """
    return cnpj_service.get_cnpj_info(cnpj)


@router.get(
    "/cnpjs/{cnpj}/activities",
    response_model=Activities,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}/activities",
    response_model=Activities,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_activities(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the main and secondary activities (CNAEs) of a CNPJ. Responds 404 if
    the CNPJ has none.
    """
    return cnpj_service.get_cnpj_activities(cnpj)


@router.get(
    "/cnpjs/{cnpj}/partners",
    response_model=Partners,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}/partners",
    response_model=Partners,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_partners(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the partners (QSA) of a CNPJ. Responds 404 if there are none, which
    is usual for sole proprietorships.
    """
    return cnpj_service.get_cnpj_partners(cnpj)


@router.get(
    "/cnpjs/{cnpj}/simples-simei",
    response_model=SimplesSimei,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}/simples-simei",
    response_model=SimplesSimei,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_simples_simei(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the Simples Nacional and SIMEI status of a CNPJ. Responds 404 if
    there is no record.
    """
    return cnpj_service.get_cnpj_simples_simei(cnpj)


@router.get(
    "/cnpjs/{cnpj}/company",
    response_model=Company,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}/company",
    response_model=Company,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_company(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the company (CNPJ base) of a CNPJ. Responds 404 if it does not exist.
    """
    return cnpj_service.get_cnpj_company(cnpj)


@router.get(
    "/cnpjs/{cnpj}/establishment",
    response_model=Establishment,
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}/establishment",
    response_model=Establishment,
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_establishment(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the establishment of a CNPJ. Responds 404 if it does not exist.
    """
    return cnpj_service.get_cnpj_establishment(cnpj)


@router.get(
    "/cnpjs/{cnpj}/establishments",
    response_model=List[Establishment],
    response_model_exclude_unset=True,
)
@router.get(
    "/cnpj/{cnpj}/establishments",
    response_model=List[Establishment],
    response_model_exclude_unset=True,
    deprecated=True,
)
@rate_limit()
def get_cnpj_establishments(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get all establishments sharing the CNPJ base (first 8 digits) of the
    given full CNPJ. Responds 404 if there are none.
    """
    return cnpj_service.get_cnpj_establishments(cnpj)


@router.get(
    "/cnpjs",
    response_model=List[CNPJRecord],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs(
    request: Request,
    query_params: CNPJQueryParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    List CNPJs matching the filters (state, city, ZIP code, CNAE, activity
    start date, headquarters only), paginated with `limit` and `offset`.
    """
    return cnpj_service.get_cnpjs(query_params)


@router.post(
    "/cnpjs",
    response_model=CNPJBatchResult,
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_info(
    request: Request,
    cnpj_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the full records for a batch of CNPJs. Invalid CNPJs are reported
    separately from the ones found.
    """
    return cnpj_service.get_cnpjs_info(cnpj_batch)


@router.post(
    "/cnpjs/partners",
    response_model=Dict[str, Partners],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_partners(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the partners (QSA) for a batch of CNPJs.
    """
    return cnpj_service.get_cnpjs_partners(cnpj_batch)


@router.post(
    "/cnpjs/company",
    response_model=Dict[str, Company],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_company(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the companies for a batch of CNPJs.
    """
    return cnpj_service.get_cnpjs_company(cnpj_batch)


@router.post(
    "/cnpjs/establishment",
    response_model=Dict[str, Establishment],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_establishment(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the establishments for a batch of CNPJs.
    """
    return cnpj_service.get_cnpjs_establishment(cnpj_batch)


@router.post(
    "/cnpjs/simples-simei",
    response_model=Dict[str, SimplesSimei],
    response_model_exclude_unset=True,
)
@rate_limit()
def get_cnpjs_simples_simei(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
) -> Dict[str, dict]:
    """
    Get the Simples Nacional and SIMEI status for a batch of CNPJs.
    """
    return cnpj_service.get_cnpjs_simples_simei(cnpj_batch)
