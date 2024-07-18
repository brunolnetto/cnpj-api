from fastapi import Depends
from fastapi.requests import Request
from jose import jwt
from time import time
from fastapi.security import OAuth2PasswordBearer

from backend.app.setup.config import settings
from backend.app.exceptions import (
    ExpiredTokenException,
    MissingTokenException,
    CustomHTTPException,
)

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

AUTH_TOKEN_URL=f"{settings.API_V1_STR}/token"

class JWTBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str = AUTH_TOKEN_URL):
        super(JWTBearer, self).__init__(tokenUrl=tokenUrl)

    async def __call__(self, request: Request):
        token = None
        authorization = request.headers.get("Authorization")

        if authorization:
            scheme, token = authorization.split()
        if not token:
            raise MissingTokenException()
        try:
            check_claims={
                "verify_aud": False, "verify_iss": False, "verify_sub": False
            }
            
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options=check_claims
            )
            
            if payload["exp"] <= time():
                raise ExpiredTokenException()

        except ExpiredTokenException:
            raise ExpiredTokenException()

        except Exception as e:
            raise CustomHTTPException(e)


jwt_bearer = JWTBearer(tokenUrl=AUTH_TOKEN_URL)

JWTDependency = Depends(jwt_bearer)
