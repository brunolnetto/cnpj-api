from typing import Union, Dict, Annotated

from fastapi import APIRouter, Request, Query

from backend.app.api.services.cnpj import CNPJService, CNPJServiceDependency
from backend.app.rate_limiter import rate_limit
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.api.models.base import BatchModel
from backend.app.api.models.cnpj import CNPJBatch, CNPJQueryParams
from backend.app.api.models.misc import LimitOffsetParams, PaginatedLimitOffsetParams 
from backend.app.setup.config import settings

# Types
CodeType = Union[str, int]

router = APIRouter(tags=["CNPJ"], dependencies=[JWTDependency])


@rate_limit()
@router.get("/cnaes")
async def get_cnaes(
    request: Request,
    query_params: Annotated[PaginatedLimitOffsetParams, Query()],
    search_token: str = "",
    cnpj_service: CNPJService = CNPJServiceDependency
    
):
    """
    Get a list of CNAEs from the database.

    Parameters:
    - limit: The maximum number of CNAEs to return.

    Returns:
    - A list of CNAEs as dictionaries.
    """
    return (
        await cnpj_service.get_cnae_by_token(search_token)
        if search_token != ""
        else await cnpj_service.get_cnaes(
            query_params.limit, query_params.offset, query_params.enable_pagination
        )
    )


@rate_limit()
@router.post("/cnaes")
async def get_cnae_objects(
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
    return await cnpj_service.get_cnae_objects(cnae_code_batch) \
        if not search_token else  cnpj_service.get_cnae_by_token(search_token)


@rate_limit()
@router.post("/cnaes/cnpjs")
async def get_cnpjs_by_cnaes(
    request: Request,
    cnae_batch: BatchModel,
    query_params: Annotated[LimitOffsetParams, Query()],
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
    return await cnpj_service.get_cnpjs_by_cnaes(
        cnae_batch, query_params.limit, query_params.offset
    )


@rate_limit()
@router.get("/cnae/{cnae_code}")
async def get_cnae_description(
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
    return await cnpj_service.get_cnae_description(cnae_code)


@rate_limit()
@router.get("/cnae/{cnae_code}/cnpjs")
async def get_cnpjs_with_cnae(
    request: Request,
    cnae_code: CodeType,
    query_params: Annotated[LimitOffsetParams, Query()],
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
    return await cnpj_service.get_cnpjs_with_cnae(
        cnae_code, query_params.limit, query_params.offset
    )


@rate_limit()
@router.post("/states/cnpjs")
async def get_cnpjs_by_state(
    request: Request,
    state_batch: BatchModel,
    query_params: Annotated[LimitOffsetParams, Query()],
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
    return await cnpj_service.get_cnpjs_by_states(
        state_batch, query_params.limit, query_params.offset
    )


@rate_limit()
@router.get("/company/sizes")
async def get_company_sizes(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a dictionary with the company sizes.

    Returns:
    - A dictionary with the company sizes.
    """
    return await cnpj_service.get_company_size_dict()


@rate_limit()
@router.get("/company/situation")
async def get_situations(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a dictionary with the company situations.

    Returns:
    - A dictionary with the company situations.
    """
    return await cnpj_service.get_company_situation_dict()


@rate_limit()
@router.get("/establishment/types")
async def get_establishment_sizes(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a dictionary with the company sizes.

    Returns:
    - A dictionary with the company sizes.
    """
    return await cnpj_service.get_establishment_type_dict()


@rate_limit()
@router.get("/city/{city_code}")
async def get_city(
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
    return await cnpj_service.get_city(city_code)


@rate_limit()
@router.get("/cities")
async def get_cities(
    request: Request,
    query_params: Annotated[LimitOffsetParams, Query()],
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of cities from the database.

    Parameters:
    - limit: The maximum number of cities to return.

    Returns:
    - A list of cities as dictionaries.
    """
    return await cnpj_service.get_cities(query_params.limit, query_params.offset)


@rate_limit()
@router.post("/cities")
async def get_cities_list(
    request: Request,
    cities_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return await cnpj_service.get_cities_list(cities_code_batch)


@rate_limit()
@router.post("/cities/infer")
async def infer_city(
    request: Request,
    city_name_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return await cnpj_service.get_city_candidates(city_name_batch)


@rate_limit()
@router.get("/legal-nature/{legal_nature_code}")
async def get_legal_nature(
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
    return await cnpj_service.get_legal_nature(legal_nature_code)


@rate_limit()
@router.get("/legal-natures")
async def get_legal_natures(
    request: Request,
    query_params: Annotated[PaginatedLimitOffsetParams, Query()],
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    return await cnpj_service.get_legal_natures(
        query_params.limit, query_params.offset, query_params.enable_pagination
    )


@rate_limit()
@router.post("/legal-natures")
async def get_legal_natures_list(
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
    return await cnpj_service.get_legal_natures_list(legal_natures_code_batch)


@rate_limit()
@router.get("/registration-status/{registration_status_code}")
async def get_registration_status(
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
    return await cnpj_service.get_registration_status(registration_status_code)


@rate_limit()
@router.get("/registration-statuses")
async def get_registration_statuses(
    request: Request,
    query_params: Annotated[PaginatedLimitOffsetParams, Query()],
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of registration statuses from the database.

    Parameters:
    - limit: The maximum number of registration statuses to return.

    Returns:
    - A list of registration statuses as dictionaries.
    """
    return await cnpj_service.get_registration_statuses(
        query_params.limit, query_params.offset, query_params.enable_pagination
    )


@rate_limit()
@router.post("/registration-statuses")
async def get_registration_statuses_list(
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
    return await cnpj_service.get_registration_statuses_list(registration_code_batch)


@rate_limit()
@router.get("/cnpj/{cnpj}")
async def get_cnpj_info(
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
    cnpj_info = await cnpj_service.get_cnpj_info(cnpj)
    return cnpj_info


@rate_limit()
@router.get("/cnpj/{cnpj}/activities")
async def get_cnpj_activities(
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
    return await cnpj_service.get_cnpj_activities(cnpj)


@rate_limit()
@router.get("/cnpj/{cnpj}/partners")
async def get_cnpj_partners(
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
    return await cnpj_service.get_cnpj_partners(cnpj)


@rate_limit()
@router.get("/cnpj/{cnpj}/simples-simei")
async def get_cnpj_simples_simei(
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


@rate_limit()
@router.get("/cnpj/{cnpj}/company")
async def get_cnpj_company(
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
    return await cnpj_service.get_cnpj_company(cnpj)


@rate_limit()
@router.get("/cnpj/{cnpj}/establishment")
async def get_cnpj_establishment(
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
    return await cnpj_service.get_cnpj_establishment(cnpj)


@rate_limit()
@router.get("/cnpj/{cnpj}/establishments")
async def get_cnpj_establishments(
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
    return await cnpj_service.get_cnpj_establishments(cnpj)


@rate_limit()
@router.get("/cnpjs")
async def get_cnpjs(
    request: Request,
    query_params: Annotated[CNPJQueryParams, Query()],
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJs from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return await cnpj_service.get_cnpjs(
        query_params.state_abbrev, 
        query_params.city_name, 
        query_params.cnae_code, 
        query_params.zipcode, 
        query_params.is_all, 
        query_params.limit, 
        query_params.offset
    )


@rate_limit()
@router.post("/cnpjs")
async def get_cnpjs_info(
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
    return await cnpj_service.get_cnpjs_info(cnpj_batch)


@rate_limit()
@router.post("/cnpjs/partners")
async def get_cnpjs_partners(
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
    return await cnpj_service.get_cnpjs_partners(cnpj_batch)


@rate_limit()
@router.post("/cnpjs/company")
async def get_cnpjs_company(
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
    return await cnpj_service.get_cnpjs_company(cnpj_batch)


@rate_limit()
@router.post("/cnpjs/establishment")
async def get_cnpjs_establishment(
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
    return await cnpj_service.get_cnpjs_establishment(cnpj_batch)


@rate_limit()
@router.post("/cnpjs/simples-simei")
async def get_cnpjs_simples_simei(
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
