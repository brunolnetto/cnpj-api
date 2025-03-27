from datetime import datetime
from datetime import timedelta
from datetime import timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from backend.app.setup.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(
        data: dict,
        expires_delta: timedelta = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    """
    Create a JSON Web Token (JWT) with the provided data and expiration time.

    Args:
        data (dict): The data to be encoded in the JWT.
        expires_delta (timedelta | None, optional): The expiration time for the JWT.
        Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT.

    """
    to_encode = data.copy()
    current_time = datetime.now(timezone.utc)

    # Set the expiration time
    expire = current_time + expires_delta

    time_data = {"exp": expire, "iat": datetime.now()}
    to_encode.update(time_data)

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt
