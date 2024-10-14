from typing import Union

from fastapi import APIRouter, Request

from backend.app.api.services.cnpj import (
    CNPJService,
    CNPJServiceDependency,
)
from backend.app.rate_limiter import limiter
from backend.app.setup.config import settings
from backend.app.api.models.cnpj import CNPJBatch
from backend.app.api.models.base import BatchModel

# Types
CodeType = Union[str, int]

router = APIRouter(tags=["CNPJ"])


@router.get("/cnaes")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnaes(
    request: Request,
    search_token: str = "",
    limit: int = 10,
    offset: int = 0,
    enable_pagination: bool = True,
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
        await cnpj_service.get_cnae_by_token(search_token)
        if search_token != ""
        else await cnpj_service.get_cnaes(limit, offset, enable_pagination)
    )


@router.post("/cnaes")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnae_objects(
    request: Request,
    search_token: str,
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


@router.post("/cnaes/cnpjs")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpjs_by_cnaes(
    request: Request,
    cnae_batch: BatchModel,
    limit: int = 10,
    offset: int = 0,
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
    return await cnpj_service.get_cnpjs_by_cnaes(cnae_batch, limit, offset)


@router.get("/cnae/{cnae_code}")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/cnae/{cnae_code}/cnpjs")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpjs_with_cnae(
    request: Request,
    cnae_code: CodeType,
    limit: int = 10,
    offset: int = 0,
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
    return await cnpj_service.get_cnpjs_with_cnae(cnae_code, limit, offset)


@router.post("/states/cnpjs")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpjs_by_state(
    request: Request,
    state_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
    limit: int = 10,
    offset: int = 0,
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
    return await cnpj_service.get_cnpjs_by_states(state_batch, limit, offset)


@router.get("/company/sizes")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/company/situation")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/establishment/types")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/city/{city_code}")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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
    from time import perf_counter

    t0 = perf_counter()
    result = await cnpj_service.get_city(city_code)
    t1 = perf_counter()
    print(f"get_city took {t1-t0:.4f} seconds")

    return result


@router.get("/cities")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cities(
    request: Request,
    cnpj_service: CNPJService = CNPJServiceDependency,
    limit: int = 10,
    offset: int = 0,
):
    """
    Get a list of cities from the database.

    Parameters:
    - limit: The maximum number of cities to return.

    Returns:
    - A list of cities as dictionaries.
    """
    from time import perf_counter

    t0 = perf_counter()
    result = await cnpj_service.get_cities(limit, offset)
    t1 = perf_counter()
    print(f"get_cities took {t1-t0:.4f} seconds")

    return result


@router.post("/cities")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cities_list(
    request: Request,
    cities_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return await cnpj_service.get_cities_list(cities_code_batch)


@router.post("/cities/infer")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def infer_city(
    request: Request,
    city_name_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return await cnpj_service.get_city_candidates(city_name_batch)


@router.get("/legal-nature/{legal_nature_code}")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/legal-natures")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_legal_natures(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    enable_pagination: bool = True,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    return await cnpj_service.get_legal_natures(limit, offset, enable_pagination)


@router.post("/legal-natures")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/registration-status/{registration_status_code}")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/registration-statuses")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_registration_statuses(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    enable_pagination: bool = True,
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
        limit, offset, enable_pagination
    )


@router.post("/registration-statuses")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.get("/cnpj/{cnpj}")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpj_info(
    request: Request, cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get information about a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the CNPJ.
    """

    return await cnpj_service.get_cnpj_info(cnpj)


@router.get("/cnpj/{cnpj}/activities")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpj_activities(
    request: Request, cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the activities of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of activities associated with the CNPJ.
    """
    return await cnpj_service.get_cnpj_activities(cnpj)


@router.get("/cnpj/{cnpj}/partners")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpj_partners(
    request: Request, cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the partners of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of partners associated with the CNPJ.
    """
    return await cnpj_service.get_cnpj_partners(cnpj)


@router.get("/cnpj/{cnpj}/company")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpj_company(
    request: Request, cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the company associated with a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the company.
    """
    return await cnpj_service.get_cnpj_company(cnpj)


@router.get("/cnpj/{cnpj}/establishment")
async def get_cnpj_establishment(
    request: Request, cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the establishment associated with a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the establishment.
    """
    from time import perf_counter

    t0 = perf_counter()
    result = await cnpj_service.get_cnpj_establishment(cnpj)
    print(f"get_cnpj_establishment took {perf_counter()-t0:.4f} seconds")

    return result


@router.get("/cnpj/{cnpj}/establishments")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpj_establishments(
    request: Request, cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
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


@router.get("/cnpjs")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def get_cnpjs(
    request: Request,
    state_abbrev: str = "",
    city_name: str = "",
    cnae_code: str = "",
    zipcode: str = "",
    is_all: bool = False,
    limit: int = 10,
    offset: int = 0,
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
        state_abbrev, city_name, cnae_code, zipcode, is_all, limit, offset
    )


@router.post("/cnpjs")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.post("/cnpjs/partners")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.post("/cnpjs/company")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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


@router.post("/cnpjs/establishment")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
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
