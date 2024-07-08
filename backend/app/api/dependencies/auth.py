from fastapi import HTTPException, status, Depends
from fastapi.requests import Request
from os import getenv
from jose import jwt
from time import time 
from fastapi.security import OAuth2PasswordBearer

from backend.app.setup.config import settings
from backend.app.exceptions import (
    ExpiredTokenException,
    MissingTokenException,
    InvalidTokenException,
    CustomHTTPException,
)

JWT_SECRET_KEY = settings.JWT_SECRET_KEY 
JWT_ALGORITHM = settings.JWT_ALGORITHM

class JWTBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str = f"{settings.API_V1_STR}/token"):
        super(JWTBearer, self).__init__(tokenUrl=tokenUrl)

    async def __call__(self, request: Request):
        token = None
        authorization = request.headers.get("Authorization")

        if authorization:
            scheme, token = authorization.split()
        if not token:
            raise MissingTokenException()

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

            if payload['exp'] <= time():
                raise ExpiredTokenException()
        
        except ExpiredTokenException:
            raise ExpiredTokenException()
        
        except Exception as e:
            raise CustomHTTPException(e)

jwt_bearer = JWTBearer(tokenUrl="token")

JWTDependency = Depends(jwt_bearer)
