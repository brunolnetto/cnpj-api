from fastapi import APIRouter

from  backend.app.api.dependencies.auth import JWTDependency

from . import auth
from . import cnpj
from . import setup

api_router = APIRouter()

# Add routers here
api_router.include_router(auth.router)
api_router.include_router(setup.router, dependencies=[JWTDependency])
api_router.include_router(cnpj.router, dependencies=[JWTDependency])
