from fastapi import APIRouter, HTTPException

from backend.repositories.cnpj import CNPJRepository
from backend.api.dependencies.cnpj import CNPJRepositoryDependency
from backend.api.models.cnpj import CNPJ
from backend.api.utils.cnpj import parse_cnpj_str, format_cnpj
from backend.api.utils.misc import check_limit_and_offset

router = APIRouter()

@router.get("/cnpjs")
async def get_cnpjs(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10, 
    offset: int = 0
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
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cnaes")
async def get_cnaes(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
    all: bool = False
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

        cnaes=cnpj_repository.get_cnaes(limit=limit, offset=offset, all=all)
        
        return cnaes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cnae/{cnae_code}")
async def get_cnae_description(
    cnae_code: str,
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
        cnaes=cnpj_repository.get_cnae(cnae_code)
        
        if len(cnaes)==0:
            raise ValueError(f"CNAE code {cnae_code} not found.")
        else:
            return cnaes
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cnae/{cnae_code}/establishments")
async def get_establishments_by_cnae(
    cnae_code: str,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0
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

        cnaes=cnpj_repository.get_cnae(cnae_code)

        if not cnaes:
            raise ValueError(f"There isn't CNAE code {cnae_code}.")
        else:
            establishments=cnpj_repository.get_establishments_by_cnae(cnae_code, limit=limit, offset=offset)

            if len(establishments)==0:
                raise ValueError(f"There are no establishents with CNAE code {cnae_code}.")
            else:
                return establishments 
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cities")
def get_cities(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0
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
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/city/{city_code}")
def get_city(
    city_code: str,
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
        city=cnpj_repository.get_city(city_code)

        if len(city)==0:
            raise ValueError(f"City code {city_code} not found.")
        else:
            return city 
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/legal-natures")
async def get_legal_natures(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
    all: bool = False
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
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/legal-nature/{legal_nature_code}")
async def get_legal_nature(
    legal_nature_code: str,
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
        legal_nature=cnpj_repository.get_legal_nature(legal_nature_code)

        if len(legal_nature)==0:
            raise ValueError(f"Legal nature code {legal_nature_code} not found.")
        else:
            return legal_nature
         
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/registration-status/{registration_status_code}")
async def get_registration_status(
    registration_status_code: str,
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
        registration_status=cnpj_repository.get_registration_status(registration_status_code)

        if len(registration_status)==0:
            raise ValueError(f"Registration status code {registration_status_code} not found.")
        else:
            return registration_status
         
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/registration-statuses")
async def get_registration_statuses(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10,
    offset: int = 0,
    all: bool = False
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

        return cnpj_repository.get_registration_statuses(limit=limit, offset=offset, all=all)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_obj=CNPJ(*cnpj_list)
        
        activities=cnpj_repository.get_activities(cnpj_obj)
        
        if(not activities):
            base="There are no activities associated with CNPJ {cnpj}."
            explanation="Try route /cnpj/{cnpj}/company to verify if the CNPJ exists."
            raise ValueError(f"{base}. {explanation}")
        else:
            return activities
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cnpj/{cnpj}/partners")
async def get_partners(
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
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_obj=CNPJ(*cnpj_list)
        cnpj_info=cnpj_repository.get_partners(cnpj_obj)

        if(not cnpj_info):
            explanation="It is likely either a sole proprietorship or a legal entity."
            msg=f"There are no partners associated with CNPJ {cnpj}. {explanation}"
            raise ValueError(msg)
        else:
            return cnpj_info
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))   


@router.get("/cnpj/{cnpj}/company")
async def get_company(
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
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_obj=CNPJ(*cnpj_list)
        company_info=cnpj_repository.get_company(cnpj_obj)

        if(not company_info):
            raise ValueError(f"There is no company associated with CNPJ {cnpj}.")
        else:
            return company_info 
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

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
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_obj=CNPJ(*cnpj_list)
        est_info=cnpj_repository.get_establishment(cnpj_obj)

        if(not est_info):
            base_msg="There is no establishment associated with CNPJ {cnpj}"
            explanation="Try route /cnpj/{cnpj}/company to verify if the CNPJ exists."
            raise ValueError(f"{base_msg}. {explanation}")
        else:
            return est_info 
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cnpj/{cnpj}/establishments")
async def get_establishments(
    cnpj: str,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the establishments associated with a CNPJ base (First 8 digits). You must provide any full CNPJ number.
    
    Parameters:
    - cnpj: The CNPJ number to search for.
    
    Returns:
    - A list of establishments associated with the CNPJ.
    """
    try:
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_base=cnpj_list[:8]
        cnpj_obj=CNPJ(*cnpj_list)

        est_info=cnpj_repository.get_establishments(cnpj_obj)

        if(not est_info):
            raise ValueError(f"There are no establishments associated with CNPJ base {cnpj_base}.")
        else:
            return est_info 
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
        cnpj_list=parse_cnpj_str(cnpj)
        
        cnpj_obj=CNPJ(*cnpj_list)
        
        cnpj_info=cnpj_repository.get_cnpj_info(cnpj_obj)
        
        if(not cnpj_info):
            formatted_cnpj=format_cnpj(cnpj)
            raise ValueError(f"CNPJ {formatted_cnpj} not found.")
        else:
            return cnpj_info
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
   