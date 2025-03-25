from pydantic import BaseModel
from pydantic import Field

from backend.app.api.constants import MAX_LIMIT
from backend.app.setup.config import settings


class LimitOffsetParams(BaseModel):
    """Pagination parameters based on limit-offset."""

    limit: int = Field(
        settings.PAGE_SIZE,
        gt=0,
        le=MAX_LIMIT,
        description="Maximum number of records to return (between 1 and 100)",
    )
    offset: int = Field(0, ge=0, description="Number of records to skip")


class PaginatedLimitOffsetParams(LimitOffsetParams):
    """Extended limit-offset parameters with optional pagination toggle."""

    enable_pagination: bool = Field(
        True, description="Enable or disable pagination")
