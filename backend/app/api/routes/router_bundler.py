from fastapi import APIRouter

from . import setup, cnpj, auth

api_router = APIRouter()

# Add routers here
api_router.include_router(auth.router)
api_router.include_router(cnpj.router)
api_router.include_router(setup.router)


