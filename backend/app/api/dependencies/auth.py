from jose import jwt
from fastapi import Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer


from backend.app.setup.config import settings
from backend.app.exceptions import (
    ExpiredTokenException,
    MissingTokenException,
    CustomHTTPException,
)

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

AUTH_TOKEN_URL = f"{settings.API_V1_STR}/token"


class JWTBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str = AUTH_TOKEN_URL):
        super().__init__(tokenUrl=tokenUrl)

    async def __call__(self, request: Request):
        authorization = request.headers.get("Authorization", "")
        try:
            scheme, token = authorization.split()
        except ValueError:
            raise MissingTokenException()
        if scheme.lower() != "bearer":
            raise MissingTokenException()

        try:
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            # jwt.decode will raise ExpiredSignatureError if the token is
            # expired
        except ExpiredTokenException:
            raise ExpiredTokenException()
        except Exception as e:
            raise CustomHTTPException(f"Invalid token: {str(e)}") from e

        return payload


jwt_bearer = JWTBearer(tokenUrl=AUTH_TOKEN_URL)

JWTDependency = Depends(jwt_bearer)
