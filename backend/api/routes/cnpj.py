from fastapi import APIRouter, HTTPException

from backend.repositories.cnpj import CNPJRepository
from backend.api.dependencies.cnpj import CNPJRepositoryDependency
from backend.api.models.cnpj import CNPJ
from backend.api.utils.cnpj import (
    parse_cnpj_str,
    format_cnpj,
    is_number,
)
from backend.api.utils.misc import check_limit_and_offset

router = APIRouter()


@router.get("/cnpjs")
async def get_cnpjs(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
):
    """
    Get a list of CNPJs from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    try:
        check_limit_and_offset(limit, offset)

        return cnpj_repository.get_cnpjs(limit=limit, offset=offset)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/cnaes")
async def get_cnaes(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
    all: bool = False,
):
    """
    Get a list of CNAEs from the database.

    Parameters:
    - limit: The maximum number of CNAEs to return.

    Returns:
    - A list of CNAEs as dictionaries.
    """
    try:
        check_limit_and_offset(limit, offset)

        cnaes = cnpj_repository.get_cnaes(limit=limit, offset=offset, all=all)

        return cnaes

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/cnae/{cnae_code}")
async def get_cnae_description(
    cnae_code: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the description of a CNAE code.

    Parameters:
    - cnae: The CNAE code to search for.

    Returns:
    - A dictionary with the CNAE description.
    """
    try:
        cnaes = cnpj_repository.get_cnae(cnae_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(cnaes) == 0:
        message = f"CNAE code {cnae_code} not found."
        raise HTTPException(status_code=404, detail=message)

    return cnaes


@router.get("/cnae/{cnae_code}/establishments")
async def get_establishments_by_cnae(
    cnae_code: str,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
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
    try:
        check_limit_and_offset(limit, offset)

        cnaes = cnpj_repository.get_cnae(cnae_code)

        if not cnaes:
            raise ValueError(f"There isn't CNAE code {cnae_code}.")

        establishments = cnpj_repository.get_establishments_by_cnae(
            cnae_code, limit=limit, offset=offset
        )

        if len(establishments) == 0:
            message = f"There are no establishents with CNAE code {cnae_code}."
            raise HTTPException(status_code=404, detail=message)

        return establishments

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/cities")
def get_cities(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
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
    try:
        check_limit_and_offset(limit, offset)

        return cnpj_repository.get_cities(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/city/{city_code}")
def get_city(
    city_code: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the name of a city code.

    Parameters:
    - city_code: The city code to search for.

    Returns:
    - A dictionary with the city name.
    """
    try:
        if not is_number(city_code):
            raise ValueError(f"City code {city_code} is not a number.")

        city = cnpj_repository.get_city(city_code)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(city) == 0:
        message = f"City code {city_code} not found."
        raise HTTPException(status_code=404, detail=message)

    return city


@router.get("/legal-natures")
async def get_legal_natures(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
    all: bool = False,
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    try:
        check_limit_and_offset(limit, offset)

        return cnpj_repository.get_legal_natures(limit=limit, offset=offset, all=all)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/legal-nature/{legal_nature_code}")
async def get_legal_nature(
    legal_nature_code: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    try:
        if not is_number(legal_nature_code):
            raise ValueError(f"Legal nature code {legal_nature_code} is not a number.")

        legal_nature = cnpj_repository.get_legal_nature(legal_nature_code)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(legal_nature) == 0:
        message = f"Legal nature code {legal_nature_code} not found."
        raise HTTPException(status_code=404, detail=message)

    return legal_nature


@router.get("/registration-status/{registration_status_code}")
async def get_registration_status(
    registration_status_code: str,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
):
    """
    Get a registration status from the database.

    Parameters:
    - registration_status_code: The registration status code to search for.

    Returns:
    - A dictionary with the registration status.
    """
    try:
        if not is_number(registration_status_code):
            raise ValueError(
                f"Registration status code {registration_status_code} is not a number."
            )

        registration_status = cnpj_repository.get_registration_status(
            registration_status_code
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(registration_status) == 0:
        message = f"Registration status code {registration_status_code} not found."
        raise HTTPException(status_code=404, detail=message)

    return registration_status


@router.get("/registration-statuses")
async def get_registration_statuses(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
    all: bool = False,
):
    """
    Get a list of registration statuses from the database.

    Parameters:
    - limit: The maximum number of registration statuses to return.

    Returns:
    - A list of registration statuses as dictionaries.
    """
    try:
        check_limit_and_offset(limit, offset)

        return cnpj_repository.get_registration_statuses(
            limit=limit, offset=offset, all=all
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/cnpj/{cnpj}/activities")
async def get_activities(
    cnpj: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the activities of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of activities associated with the CNPJ.
    """
    try:
        if not is_number(cnpj):
            raise ValueError(
                f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
            )

        cnpj_list = parse_cnpj_str(cnpj)
        cnpj_obj = CNPJ(*cnpj_list)

        activities = cnpj_repository.get_activities(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not activities:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return activities


@router.get("/cnpj/{cnpj}/partners")
async def get_partners(
    cnpj: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the partners of a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of partners associated with the CNPJ.
    """
    try:
        if not is_number(cnpj):
            raise ValueError(
                f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
            )

        cnpj_list = parse_cnpj_str(cnpj)
        cnpj_obj = CNPJ(*cnpj_list)
        cnpj_info = cnpj_repository.get_partners(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not cnpj_info:
        error = f"There are no partners associated with CNPJ {cnpj}"
        explanation = "It is likely either a sole proprietorship or a legal entity."
        msg = f"{error}. {explanation}"
        raise HTTPException(status_code=404, detail=msg)

    return cnpj_info


@router.get("/cnpj/{cnpj}/company")
async def get_company(
    cnpj: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the company associated with a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the company.
    """
    try:
        if not is_number(cnpj):
            raise ValueError(
                f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
            )

        cnpj_list = parse_cnpj_str(cnpj)
        cnpj_obj = CNPJ(*cnpj_list)
        company_info = cnpj_repository.get_company(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not company_info:
        message = f"There is no company associated with CNPJ {cnpj}."
        raise HTTPException(status_code=404, detail=message)

    return company_info


@router.get("/cnpj/{cnpj}/establishment")
async def get_establishment(
    cnpj: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        cnpj_list = parse_cnpj_str(cnpj)
        cnpj_obj = CNPJ(*cnpj_list)
        est_info = cnpj_repository.get_establishment(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not est_info:
        base_msg = f"There is no establishment associated with CNPJ {cnpj}"
        explanation = f"Try route /cnpj/{cnpj}/company to verify if the CNPJ exists."
        message = f"{base_msg}. {explanation}"

        raise HTTPException(status_code=404, detail=message)

    return est_info


@router.get("/cnpj/{cnpj}/establishments")
async def get_establishments(
    cnpj: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the establishments associated with a CNPJ base (First 8 digits). You must provide any full CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A list of establishments associated with the CNPJ.
    """
    try:
        if not is_number(cnpj):
            raise ValueError(
                f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
            )

        cnpj_list = parse_cnpj_str(cnpj)
        cnpj_base = cnpj_list[:8]
        cnpj_obj = CNPJ(*cnpj_list)

        est_info = cnpj_repository.get_establishments(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not est_info:
        message = f"There are no establishments associated with CNPJ base {cnpj_base}."

        raise HTTPException(status_code=404, detail=message)

    return est_info


@router.get("/cnpj/{cnpj}")
async def get_cnpj_info(
    cnpj: str, cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get information about a CNPJ number.

    Parameters:
    - cnpj: The CNPJ number to search for.

    Returns:
    - A dictionary with information about the CNPJ.
    """
    try:
        if not is_number(cnpj):
            raise ValueError(
                f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
            )

        cnpj_list = parse_cnpj_str(cnpj)
        cnpj_obj = CNPJ(*cnpj_list)
        cnpj_info = cnpj_repository.get_cnpj_info(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not cnpj_info:
        formatted_cnpj = format_cnpj(cnpj)
        message = f"CNPJ {formatted_cnpj} not found."

        raise HTTPException(status_code=404, detail=message)

    return cnpj_info
