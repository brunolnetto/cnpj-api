from fastapi import APIRouter, HTTPException, Request, status
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from backend.app.api.rate_limiter import rate_limit
from backend.app.api.repositories.auth import ApiClientRepository
from backend.app.database.base import get_session
from backend.app.setup.config import settings
from backend.app.utils.security import create_token

# Public on purpose: this is where clients exchange credentials for a token
router = APIRouter(tags=["Authentication"])


class ClientCredentials(BaseModel):
    """Credentials issued to an API client."""

    client_id: str = Field(..., min_length=1, max_length=64)
    client_secret: str = Field(..., min_length=1, max_length=256)


class TokenResponse(BaseModel):
    """Response model for token generation."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token lifetime in seconds")


def _authenticate(client_id: str, client_secret: str) -> bool:
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        client = ApiClientRepository(session).authenticate(client_id, client_secret)
        return client is not None


@router.post("/token", response_model=TokenResponse)
@rate_limit()
async def generate_token(
    request: Request, credentials: ClientCredentials
) -> TokenResponse:
    """
    Exchange client credentials for an access token.

    Send the returned token as `Authorization: Bearer <access_token>`.
    """
    is_authenticated = await run_in_threadpool(
        _authenticate, credentials.client_id, credentials.client_secret
    )

    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials.",
        )

    access_token = create_token({"sub": credentials.client_id})

    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
