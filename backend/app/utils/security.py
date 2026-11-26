import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from jose import jwt

from backend.app.setup.config import settings


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JSON Web Token (JWT) with the provided data and expiration time.

    Args:
        data (dict): The data to be encoded in the JWT.
        expires_delta (timedelta | None, optional): The expiration time for the JWT.
        Defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT.

    """
    to_encode = data.copy()
    current_time = datetime.now(timezone.utc)

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = current_time + expires_delta

    time_data = {"exp": expire, "iat": current_time}
    to_encode.update(time_data)

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def generate_client_credentials() -> Tuple[str, str]:
    """
    Generate a new client id and secret.

    The secret is shown once to whoever creates the client; only its hash is stored.
    """
    client_id = f"cli_{secrets.token_hex(8)}"
    client_secret = secrets.token_urlsafe(32)

    return client_id, client_secret


def hash_client_secret(client_secret: str) -> str:
    """
    Hash a client secret for storage.

    Secrets are 256-bit random values, so a fast hash is enough: there is no
    low-entropy input for a slow hash to protect against brute force.
    """
    return hashlib.sha256(client_secret.encode("utf-8")).hexdigest()


def verify_client_secret(client_secret: str, secret_hash: str) -> bool:
    """Check a client secret against its stored hash in constant time."""
    return hmac.compare_digest(hash_client_secret(client_secret), secret_hash)
