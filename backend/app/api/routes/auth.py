from fastapi import APIRouter, Request

from backend.app.utils.security import create_token
from backend.app.api.dependencies.auth import JWTDependency

router = APIRouter(tags=["Authentication"], dependencies=[JWTDependency])


@router.get("/token")
async def get_token(request: Request):
    signature_dict = {"message": "Suas Vendas rocks!"}
    return {
        "access_token": create_token(signature_dict),
    }
