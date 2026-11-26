from typing import Union, Dict

from fastapi import APIRouter, Request, Depends

from backend.app.api.services.cnpj import CNPJService, CNPJServiceDependency
from backend.app.api.rate_limiter import rate_limit
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.api.models.base import BatchModel
from backend.app.api.models.cnpj import CNPJBatch, CNPJQueryParams
from backend.app.api.models.misc import LimitOffsetParams, PaginatedLimitOffsetParams

# Types
CodeType = Union[str, int]

router = APIRouter(tags=["CNPJ"], dependencies=[JWTDependency])


@router.get("/cnaes")
@rate_limit()
def get_cnaes(
    request: Request,
    query_params: PaginatedLimitOffsetParams = Depends(),
    search_token: str = "",
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNAEs from the database.

    Parameters:
    - limit: The maximum number of CNAEs to return.

    Returns:
    - A list of CNAEs as dictionaries.
    """
    return (
        cnpj_service.get_cnae_by_token(search_token)
        if search_token != ""
        else cnpj_service.get_cnaes(query_params)
    )


@router.post("/cnaes")
@rate_limit()
def get_cnae_objects(
    request: Request,
    cnae_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get CNAE objects from a list of codes.

    Parameters:
    - cnae: The CNAE code to search for.

    Returns:
    - A list with the CNAE objects.
    """
    return cnpj_service.get_cnae_objects(cnae_code_batch)


@router.post("/cnaes/cnpjs")
@rate_limit()
def get_cnpjs_by_cnaes(
    request: Request,
    cnae_batch: BatchModel,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of establishments by CNAE code.

    Parameters:
    - cnae_code: The CNAE code to search for.
    - limit: The maximum number of establishments to return.
    - offset: The number of establishments to skip.

    Returns:
    - A list of establishments as dictionaries.
    """
    return cnpj_service.get_cnpjs_by_cnaes(cnae_batch, query_params)


@router.get("/cnae/{cnae_code}")
@rate_limit()
def get_cnae_description(
    request: Request,
    cnae_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the description of a CNAE code.

    Parameters:
    - cnae: The CNAE code to search for.

    Returns:
    - A dictionary with the CNAE description.
    """
    return cnpj_service.get_cnae_description(cnae_code)


@router.get("/cnae/{cnae_code}/cnpjs")
@rate_limit()
def get_cnpjs_with_cnae(
    request: Request,
    cnae_code: CodeType,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of establishments with a given CNAE code.

    Parameters:
    - cnae_code: The CNAE code to search for.
    - limit: The maximum number of establishments to return.
    - offset: The number of establishments to skip.

    Returns:
    - A list of establishments as dictionaries.
    """
    return cnpj_service.get_cnpjs_with_cnae(cnae_code, query_params)


@router.post("/states/cnpjs")
@rate_limit()
def get_cnpjs_by_state(
    request: Request,
    state_batch: BatchModel,
    query_params: LimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of establishments by state code.

    Parameters:
    - state_code: The state code to search for.
    - limit: The maximum number of establishments to return.
    - offset: The number of establishments to skip.

    Returns:
    - A list of establishments as dictionaries.
    """
    return cnpj_service.get_cnpjs_by_states(
        state_batch, query_params.limit, query_params.offset
    )


@router.get("/company/sizes")
@rate_limit()
def get_company_sizes(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a dictionary with the company sizes.

    Returns:
    - A dictionary with the company sizes.
    """
    return cnpj_service.get_company_size_dict()


@router.get("/company/situation")
@rate_limit()
def get_situations(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a dictionary with the company situations.

    Returns:
    - A dictionary with the company situations.
    """
    return cnpj_service.get_company_situation_dict()


@router.get("/establishment/types")
@rate_limit()
def get_establishment_sizes(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a dictionary with the company sizes.

    Returns:
    - A dictionary with the company sizes.
    """
    return cnpj_service.get_establishment_type_dict()


@router.get("/city/{city_code}")
@rate_limit()
def get_city(
    request: Request,
    city_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the name of a city code.

    Parameters:
    - city_code: The city code to search for.

    Returns:
    - A dictionary with the city name.
    """
    return cnpj_service.get_city(city_code)


@router.get("/cities")
@rate_limit()
def get_cities(
    request: Request,
    query_params: LimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of cities from the database.

    Parameters:
    - limit: The maximum number of cities to return.

    Returns:
    - A list of cities as dictionaries.
    """
    return cnpj_service.get_cities(query_params.limit, query_params.offset)


@router.post("/cities")
@rate_limit()
def get_cities_list(
    request: Request,
    cities_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return cnpj_service.get_cities_list(cities_code_batch)


@router.post("/cities/infer")
@rate_limit()
def infer_city(
    request: Request,
    city_name_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return cnpj_service.get_city_candidates(city_name_batch)


@router.get("/legal-nature/{legal_nature_code}")
@rate_limit()
def get_legal_nature(
    request: Request,
    legal_nature_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    return cnpj_service.get_legal_nature(legal_nature_code)


@router.get("/legal-natures")
@rate_limit()
def get_legal_natures(
    request: Request,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    return cnpj_service.get_legal_natures(query_params)


@router.post("/legal-natures")
@rate_limit()
def get_legal_natures_list(
    request: Request,
    legal_natures_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    return cnpj_service.get_legal_natures_list(legal_natures_code_batch)


@router.get("/registration-status/{registration_status_code}")
@rate_limit()
def get_registration_status(
    request: Request,
    registration_status_code: CodeType,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a registration status from the database.

    Parameters:
    - registration_status_code: The registration status code to search for.

    Returns:
    - A dictionary with the registration status.
    """
    return cnpj_service.get_registration_status(registration_status_code)


@router.get("/registration-statuses")
@rate_limit()
def get_registration_statuses(
    request: Request,
    query_params: PaginatedLimitOffsetParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of registration statuses from the database.

    Parameters:
    - limit: The maximum number of registration statuses to return.

    Returns:
    - A list of registration statuses as dictionaries.
    """
    return cnpj_service.get_registration_statuses(query_params)


@router.post("/registration-statuses")
@rate_limit()
def get_registration_statuses_list(
    request: Request,
    registration_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of registration statuses from the database.

    Parameters:
    - code_list: The list of registration status codes to search for.

    Returns:
    - A list of registration statuses as dictionaries.
    """
    return cnpj_service.get_registration_statuses_list(registration_code_batch)


@router.get("/cnpj/{cnpj}")
@rate_limit()
def get_cnpj_info(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get information about a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the CNPJ.
    """
    return cnpj_service.get_cnpj_info(cnpj)


@router.get("/cnpj/{cnpj}/activities")
@rate_limit()
def get_cnpj_activities(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the activities of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of activities associated with the CNPJ.
    """
    return cnpj_service.get_cnpj_activities(cnpj)


@router.get("/cnpj/{cnpj}/partners")
@rate_limit()
def get_cnpj_partners(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the partners of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of partners associated with the CNPJ.
    """
    return cnpj_service.get_cnpj_partners(cnpj)


@router.get("/cnpj/{cnpj}/simples-simei")
@rate_limit()
def get_cnpj_simples_simei(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get Simples and SIMEI of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of partners associated with the CNPJ.
    """
    return cnpj_service.get_cnpj_simples_simei(cnpj)


@router.get("/cnpj/{cnpj}/company")
@rate_limit()
def get_cnpj_company(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the company associated with a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the company.
    """
    return cnpj_service.get_cnpj_company(cnpj)


@router.get("/cnpj/{cnpj}/establishment")
@rate_limit()
def get_cnpj_establishment(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the establishment associated with a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the establishment.
    """
    return cnpj_service.get_cnpj_establishment(cnpj)


@router.get("/cnpj/{cnpj}/establishments")
@rate_limit()
def get_cnpj_establishments(
    request: Request,
    cnpj: str,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get the establishments associated with a CNPJ base (First 8 digits).
    You must provide any full CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of establishments associated with the CNPJ.
    """
    return cnpj_service.get_cnpj_establishments(cnpj)


@router.get("/cnpjs")
@rate_limit()
def get_cnpjs(
    request: Request,
    query_params: CNPJQueryParams = Depends(),
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJs from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return cnpj_service.get_cnpjs(query_params)


@router.post("/cnpjs")
@rate_limit()
def get_cnpjs_info(
    request: Request,
    cnpj_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJs from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return cnpj_service.get_cnpjs_info(cnpj_batch)


@router.post("/cnpjs/partners")
@rate_limit()
def get_cnpjs_partners(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return cnpj_service.get_cnpjs_partners(cnpj_batch)


@router.post("/cnpjs/company")
@rate_limit()
def get_cnpjs_company(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return cnpj_service.get_cnpjs_company(cnpj_batch)


@router.post("/cnpjs/establishment")
@rate_limit()
def get_cnpjs_establishment(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return cnpj_service.get_cnpjs_establishment(cnpj_batch)


@router.post("/cnpjs/simples-simei")
@rate_limit()
def get_cnpjs_simples_simei(
    request: Request,
    cnpj_batch: CNPJBatch,
    cnpj_service: CNPJService = CNPJServiceDependency,
) -> Dict[str, dict]:
    """

    Get a list of CNPJ Simples and SIMEI information from the database.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return cnpj_service.get_cnpjs_simples_simei(cnpj_batch)
