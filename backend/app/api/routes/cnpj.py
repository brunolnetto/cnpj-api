from fastapi import APIRouter, HTTPException
from typing import Union

from backend.app.repositories.cnpj import CNPJRepository
from backend.app.api.dependencies.cnpj import CNPJRepositoryDependency

from backend.app.api.services.cnpj import CNPJService
from backend.app.api.services.cnpj import CNPJServiceDependency

from backend.app.api.models.cnpj import CNPJ
from backend.app.api.utils.cnpj import parse_cnpj_str, format_cnpj
from backend.app.utils.misc import is_number, are_numbers
from backend.app.api.utils.misc import check_limit_and_offset
from backend.app.api.models.cnpj import CNPJBatch
from backend.app.api.models.base import BatchModel
from backend.app.setup.config import settings

# Types
CodeType = Union[str, int]

router = APIRouter()


@router.get("/cnaes")
async def get_cnaes(
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
    return await cnpj_service.get_cnaes(limit, offset, enable_pagination)


@router.post("/cnaes")
async def get_cnae_objects(
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
    return await cnpj_service.get_cnae_objects(cnae_code_batch)
    

@router.get("/cnae/{cnae_code}")
async def get_cnae_description(
    cnae_code: CodeType, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the description of a CNAE code.

    Parameters:
    - cnae: The CNAE code to search for.

    Returns:
    - A dictionary with the CNAE description.
    """
    return await cnpj_service.get_cnae_description(cnae_code)


@router.get("/cnae/{cnae_code}/establishments")
async def get_establishments_by_cnae(
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
    return await cnpj_service.get_establishments_by_cnae(cnae_code, limit, offset)


@router.get("/city/{city_code}")
async def get_city(
    city_code: CodeType, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the name of a city code.

    Parameters:
    - city_code: The city code to search for.

    Returns:
    - A dictionary with the city name.
    """
    return await cnpj_service.get_city(city_code)

@router.get("/cities")
async def get_cities(
    limit: int = 10,
    offset: int = 0,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of cities from the database.

    Parameters:
    - limit: The maximum number of cities to return.

    Returns:
    - A list of cities as dictionaries.
    """
    return await cnpj_service.get_cities(limit, offset)


@router.post("/cities")
async def get_cities_list(
    cities_code_batch: BatchModel,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    return await cnpj_service.get_cities_list(cities_code_batch)


@router.get("/legal-nature/{legal_nature_code}")
async def get_legal_nature(
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
async def get_legal_natures(
    limit: int = 10, offset: int = 0, enable_pagination: bool = True,
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
async def get_legal_natures_list(
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
async def get_registration_status(
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


@router.post("/registration-statuses")
async def get_registration_statuses_list(
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


@router.get("/registration-statuses")
async def get_registration_statuses(
    limit: int = 10, offset: int = 0, enable_pagination: bool = True,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of registration statuses from the database.

    Parameters:
    - limit: The maximum number of registration statuses to return.

    Returns:
    - A list of registration statuses as dictionaries.
    """
    return await cnpj_service.get_registration_statuses(limit, offset, enable_pagination)


@router.get("/cnpj/{cnpj}")
async def get_cnpj_info(
    cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
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
async def get_activities(
    cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the activities of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of activities associated with the CNPJ.
    """
    return await cnpj_service.get_activities(cnpj)

@router.get("/cnpj/{cnpj}/partners")
async def get_cnpj_partners(
    cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
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
async def get_cnpj_company(
    cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
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
async def get_establishment(
    cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the establishment associated with a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the establishment.
    """
    try:
        if not is_number(cnpj):
            raise ValueError(
                f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
            )

        cnpj_obj = cnpj_str_to_obj(cnpj)

        est_info = cnpj_service.get_establishment(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not est_info:
        base_msg = f"There is no establishment associated with CNPJ {cnpj_obj}"
        explanation = f"Try route {settings.API_V1_STR}/cnpj/{cnpj}/company to verify if the CNPJ exists."
        message = f"{base_msg}. {explanation}"

        return {"detail": message}

    return est_info


@router.get("/cnpj/{cnpj}/establishments")
async def get_establishments(
    cnpj: str, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get the establishments associated with a CNPJ base (First 8 digits).
    You must provide any full CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of establishments associated with the CNPJ.
    """
    return await cnpj_service.get_establishments(cnpj)


@router.get("/cnpjs")
async def get_cnpjs(
    limit: int = 10, offset: int = 0,
    cnpj_service: CNPJService = CNPJServiceDependency,
):
    """
    Get a list of CNPJs from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return await cnpj_service.get_cnpjs(limit, offset)


@router.post("/cnpjs/partners")
async def get_cnpjs_partners(
    cnpj_batch: CNPJBatch, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return await cnpj_service.get_cnpj_partners(cnpj_batch)


@router.post("/cnpjs/company")
async def get_cnpjs_company(
    cnpj_batch: CNPJBatch, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return await cnpj_service.get_cnpj_company(cnpj_batch)


@router.post("/cnpjs/establishment")
async def get_cnpjs_establishment(
    cnpj_batch: CNPJBatch, cnpj_service: CNPJService = CNPJServiceDependency
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    return await cnpj_service.get_cnpjs_establishment(cnpj_batch)   