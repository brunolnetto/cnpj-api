from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from backend.app.utils.security import create_token
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.api.rate_limiter import rate_limit
from backend.app.setup.config import settings

router = APIRouter(
    tags=["Authentication"], dependencies=[JWTDependency]
)


class TokenResponse(BaseModel):
    """Response model for token generation."""

    access_token: str


# Consider configuring the rate limiter if necessary
@rate_limit()  
@router.get("/token", response_model=TokenResponse)
async def generate_token(request: Request) -> TokenResponse:
    """
    Generate a new access token.

    This endpoint generates a new access token for the user.
    """
    try:
        payload={"message": settings.SIGNATURE}
        access_token = create_token(payload)
        return TokenResponse(access_token=access_token)
    except Exception:
        # Handle any potential errors (e.g., token generation failure)
        raise HTTPException(
            status_code=500, 
            detail="Could not generate token"
        )
