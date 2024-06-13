from fastapi import APIRouter, Depends, Request

from backend.repositories.cnpj import CNPJRepository
from backend.api.dependencies.cnpj import CNPJRepositoryDependency
from backend.api.models.cnpj import CNPJ
from backend.api.utils.cnpj import parse_cnpj_str

router = APIRouter()

@router.get("/client-info")
async def read_item(request: Request):
    headers = request.headers
    
    # Access other request attributes as needed (e.g., headers, body)
    return {
        "client": request.client,
        "base_url": request.base_url,
        "url": request.url,
        "method": request.method,
        "query_params": request.query_params,
        "path_params": request.path_params,
        "headers": headers,
        "cookies": request.cookies,
        "body": await request.body()
    }

@router.get("/cnpj")
async def get_cnpjs(
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency,
    limit: int = 10
):
    """
    Get a list of CNPJs from the database.
    
    Parameters:
    - limit: The maximum number of CNPJs to return.
    
    Returns:
    - A list of CNPJs as dictionaries.
    """
    cnpjs=cnpj_repository.get_cnpjs(limit=limit)
    
    return cnpjs.to_dict(orient='records')


# Example route handler with CNPJRepository dependency
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
        
        cnpj_obj=CNPJ(
            int(cnpj_list[0]), 
            int(cnpj_list[1]), 
            int(cnpj_list[2])
        )
        
        
        return cnpj_obj.__dict__()
        
    except ValueError as e:
        return {"error": str(e)}
    
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
        
        return activities
        
    except ValueError as e:
        return {"error": str(e)}
    
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
        
        partners=cnpj_repository.get_partners(cnpj_obj)
        
        return partners
        
    except ValueError as e:
        return {"error": str(e)}
    
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
        
        company=cnpj_repository.get_company(cnpj_obj)
        
        return company
        
    except ValueError as e:
        return {"error": str(e)}
    
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
        
        establishment=cnpj_repository.get_establishment(cnpj_obj)
        
        return establishment
        
    except ValueError as e:
        return {"error": str(e)}
    

@router.get("/cnpj/{cnpj}/establishments")
async def get_establishments_with_cnae(
    cnpj: str,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the establishments associated with a CNPJ number.
    
    Parameters:
    - cnpj: The CNPJ number to search for.
    
    Returns:
    - A list of establishments associated with the CNPJ.
    """
    try:
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_obj=CNPJ(*cnpj_list)
        
        establishments=cnpj_repository.get_establishments_with_cnae(cnpj_obj)
        
        return establishments
        
    except ValueError as e:
        return {"error": str(e)}


@router.get("/cnpj/{cnpj}/cnae")
async def get_cnae_description(
    cnpj: str,
    cnpj_repository: CNPJRepository = CNPJRepositoryDependency
):
    """
    Get the CNAE description associated with a CNPJ number.
    
    Parameters:
    - cnpj: The CNPJ number to search for.
    
    Returns:
    - A dictionary with the CNAE description.
    """
    try:
        cnpj_list=parse_cnpj_str(cnpj)
        cnpj_obj=CNPJ(*cnpj_list)
        
        cnae=cnpj_repository.get_cnae_description(cnpj_obj)
        
        return cnae
        
    except ValueError as e:
        return {"error": str(e)}
