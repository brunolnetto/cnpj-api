from fastapi import APIRouter, Request

from backend.app.utils.security import create_token
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.rate_limiter import rate_limit
from backend.app.setup.config import settings

router = APIRouter(tags=["Authentication"], dependencies=[JWTDependency])


@rate_limit()
@router.get("/token")
async def get_token(request: Request):
    signature_dict = {"message": "Suas Vendas rocks!"}
    return {
        "access_token": create_token(signature_dict),
    }
