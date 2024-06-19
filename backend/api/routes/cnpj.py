from fastapi import APIRouter, HTTPException
from typing import List, Union

from backend.repositories.cnpj import CNPJRepository
from backend.api.dependencies.cnpj import CNPJRepositoryDependency
from backend.api.models.cnpj import CNPJ
from backend.api.utils.cnpj import parse_cnpj_str, format_cnpj
from backend.utils.misc import is_number, are_numbers
from backend.api.utils.misc import check_limit_and_offset
from backend.api.models.cnpj import CNPJBatch, CNPJ
from backend.api.models.base import BatchModel
from backend.setup.config import settings

# Types
CodeType=Union[str, int]

router = APIRouter()


def cnpj_str_to_obj(cnpj_str: str):
    """
    Converts a CNPJ string to a CNPJ object.

    Args:
        cnpj_str (str): The CNPJ string to convert.

    Returns:
        CNPJ: The CNPJ object.
    """
    
    cnpj_list = parse_cnpj_str(cnpj_str)
    return CNPJ(*cnpj_list)


@router.get("/cnaes")
async def get_cnaes(
    limit: int = 10,
    offset: int = 0,
    enable_pagination: bool = True,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
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

        cnaes = cnpj_repository.get_cnaes(limit=limit, offset=offset, enable_pagination=enable_pagination)

        return cnaes

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/cnaes")
async def get_cnaes_object(
    cnae_code_batch: BatchModel, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get CNAE objects from a list of codes.

    Parameters:
    - cnae: The CNAE code to search for.

    Returns:
    - A list with the CNAE objects.
    """
    try:
        cnae_code_list=cnae_code_batch.batch
        
        if not are_numbers(cnae_code_list):
            not_number_map=lambda candidate: not is_number(candidate)
            not_numbers=list(filter(not_number_map, cnae_code_list))
            raise ValueError(
                f"CNAE codes {not_numbers} are not numbers."
            )
        
        cnaes = cnpj_repository.get_cnae_list(cnae_code_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(cnaes) == 0:
        return {"detail": f"CNAE codes {cnae_code_list} not found."}

    return cnaes


@router.get("/cnae/{cnae_code}")
async def get_cnae_description(
    cnae_code: CodeType, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the description of a CNAE code.

    Parameters:
    - cnae: The CNAE code to search for.

    Returns:
    - A dictionary with the CNAE description.
    """
    try:
        if not is_number(cnae_code):
            raise ValueError(f"CNAE code {cnae_code} is not a number.")
        
        cnae_code_list=[cnae_code]
        cnaes = cnpj_repository.get_cnae_list(cnae_code_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(cnaes) == 0:
        return {"detail": f"CNAE code {cnae_code} not found."}

    return cnaes[0]


@router.get("/cnae/{cnae_code}/establishments")
async def get_establishments_by_cnae(
    cnae_code: CodeType,
    limit: int = 10,
    offset: int = 0,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(establishments) == 0:
        return {"detail": f"There are no establishents with CNAE code {cnae_code}."}

    return establishments


@router.get("/city/{city_code}")
def get_city(
    city_code: CodeType, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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
        return {"detail": f"City code {city_code} not found."}

    return city


@router.get("/cities")
def get_cities(
    limit: int = 10,
    offset: int = 0,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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


@router.post("/cities")
def get_cities_list(
    cities_code_batch: BatchModel,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    try:
        cities_code_list=list(set(cities_code_batch.batch))
        
        if not are_numbers(cities_code_list):
            not_number_map=lambda candidate: not is_number(candidate)
            not_numbers=list(filter(not_number_map, cities_code_list))
            raise ValueError(
                f"Cities codes {not_numbers} are not numbers."
            )
        
        cities_objs = cnpj_repository.get_cities_list(cities_code_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(cities_objs) == 0:
        return {"detail": f"Cities codes {cities_code_list} not found."}

    return cities_objs


@router.get("/legal-nature/{legal_nature_code}")
async def get_legal_nature(
    legal_nature_code: CodeType, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        legal_nature_code_list=[legal_nature_code]
        legal_nature_obj_list = cnpj_repository.get_legal_natures_list(legal_nature_code_list)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(legal_nature_obj_list) != 1:
        return {"detail": f"Legal nature code {legal_nature_code} not found."}

    return legal_nature_obj_list[0]


@router.get("/legal-natures")
async def get_legal_natures(
    limit: int = 10,
    offset: int = 0,
    enable_pagination: bool = True,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        return cnpj_repository.get_legal_natures(
            limit=limit, offset=offset, 
            enable_pagination=enable_pagination
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/legal-natures")
async def get_legal_natures_list(
    legal_natures_code_batch: BatchModel,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get a list of legal natures from the database.

    Parameters:
    - limit: The maximum number of legal natures to return.

    Returns:
    - A list of legal natures as dictionaries.
    """
    try:
        legal_natures_code_list=list(set(legal_natures_code_batch.batch))
        
        if not are_numbers(legal_natures_code_list):
            not_number_map=lambda candidate: not is_number(candidate)
            not_numbers=list(filter(not_number_map, legal_natures_code_list))
            raise ValueError(
                f"Cities codes {not_numbers} are not numbers."
            )

        legal_natures_objs = cnpj_repository.get_legal_natures_list(legal_natures_code_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(legal_natures_objs) == 0:
        return {"detail": f"Legal nature codes {legal_natures_code_list} not found."}

    return legal_natures_objs


@router.get("/registration-status/{registration_status_code}")
async def get_registration_status(
    registration_status_code: CodeType,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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
        
        registration_status_code=registration_status_code.strip()
        registration_status_list=[registration_status_code]
        
        registration_map=cnpj_repository.get_registration_status_list
        registration_status = registration_map(registration_status_list)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(registration_status) == 0:
        return {
            "detail": f"Registration status code {registration_status_code} not found."
        }
    
    return registration_status[0]


@router.post("/registration-statuses")
async def get_registration_statuses_list(
    registration_code_batch: BatchModel,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get a list of registration statuses from the database.

    Parameters:
    - code_list: The list of registration status codes to search for.

    Returns:
    - A list of registration statuses as dictionaries.
    """
    try:
        registration_code_list=registration_code_batch.batch
        
        if not are_numbers(registration_code_list):
            not_number_map=lambda candidate: not is_number(candidate)
            not_numbers=list(filter(not_number_map, registration_code_list))
            raise ValueError(
                f"Registration status codes {not_numbers} are not numbers."
            )
        
        registration_map=cnpj_repository.get_registration_status_list
        registration_status = registration_map(registration_code_list)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if len(registration_status) == 0:
        return {
            "detail": f"Registration status codes {registration_code_list} not found."
        }
    
    return registration_status


@router.get("/registration-statuses")
async def get_registration_statuses(
    limit: int = 10,
    offset: int = 0,
    enable_pagination: bool = True,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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
            limit=limit, offset=offset, enable_pagination=enable_pagination
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/cnpj/{cnpj}")
async def get_cnpj_info(
    cnpj: str, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        cnpj_obj = cnpj_str_to_obj(cnpj)
        cnpj_info = cnpj_repository.get_cnpj_info(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not cnpj_info:
        formatted_cnpj = format_cnpj(cnpj)
        message = f"CNPJ {formatted_cnpj} not found."

        return {"detail": message}

    return cnpj_info


@router.get("/cnpj/{cnpj}/activities")
async def get_activities(
    cnpj: str, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        cnpj_obj = cnpj_str_to_obj(cnpj)
        activities = cnpj_repository.get_activities(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not activities:
        return {"detail": f"There are no activities associated with CNPJ {cnpj}."}

    return activities


@router.get("/cnpj/{cnpj}/partners")
async def get_cnpj_partners(
    cnpj: str, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        cnpj_obj = cnpj_str_to_obj(cnpj)
        cnpj_list=[cnpj_obj]
        cnpj_info = cnpj_repository.get_cnpjs_partners(cnpj_list)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not cnpj_info:
        error = f"There are no partners associated with CNPJ {cnpj}"
        explanation = "It is likely either a sole proprietorship or a legal entity."
        msg = f"{error}. {explanation}"
        return {"detail": msg}

    cnpj_base=cnpj_obj.basico_str
    return cnpj_info[cnpj_base]


@router.get("/cnpj/{cnpj}/company")
async def get_cnpj_company(
    cnpj: str, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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

        cnpj_obj = cnpj_str_to_obj(cnpj)
        cnpj_list=[cnpj_obj]
        
        company_info=cnpj_repository.get_cnpjs_company(cnpj_list)
        
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not company_info:
        message = f"There is no company associated with CNPJ {cnpj}."
        return {"detail": message}

    cnpj_base=cnpj_obj.basico_str
    
    return company_info[cnpj_base]


@router.get("/cnpj/{cnpj}/establishment")
async def get_establishment(
    cnpj: str, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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
        
        est_info = cnpj_repository.get_cnpj_establishment(cnpj_obj)

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
    cnpj: str, 
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the establishments associated with a CNPJ base (First 8 digits).
    You must provide any full CNPJ number.

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

        cnpj_obj = cnpj_str_to_obj(cnpj)
        cnpj_base=cnpj_obj.basico_str
        
        est_info = cnpj_repository.get_cnpj_establishments(cnpj_obj)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if not est_info:
        return {
            "detail": f"There are no establishments associated with CNPJ base {cnpj_base}."
        }

    return est_info


@router.get("/cnpjs")
async def get_cnpjs(
    limit: int = 10,
    offset: int = 0,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
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
    

@router.post("/cnpjs/partners")
async def get_cnpjs_partners(
    cnpj_batch: CNPJBatch,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    try:
        cnpj_objs=set(map(cnpj_str_to_obj, cnpj_batch.batch))
        
        return cnpj_repository.get_cnpjs_partners(cnpj_objs)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/cnpjs/company")
async def get_cnpjs_company(
    cnpj_batch: CNPJBatch,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    try:
        cnpj_objs=set(map(cnpj_str_to_obj, cnpj_batch.batch))
        
        return cnpj_repository.get_cnpjs_company(cnpj_objs)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/cnpjs/establishment")
async def get_cnpjs_establishment(
    cnpj_batch: CNPJBatch,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get a list of CNPJ partners information from the database.

    Parameters:
    - limit: The maximum number of CNPJs to return.

    Returns:
    - A list of CNPJs as dictionaries.
    """
    try:
        cnpj_objs=list(map(cnpj_str_to_obj, cnpj_batch.batch))
        est_objs=cnpj_repository.get_cnpjs_establishment(cnpj_objs)
        
        return est_objs

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
