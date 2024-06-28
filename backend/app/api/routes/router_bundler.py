from fastapi import APIRouter

from . import setup, cnpj

api_router = APIRouter()

# Add routers here
api_router.include_router(setup.router)
api_router.include_router(cnpj.router)
