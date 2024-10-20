from pydantic import BaseModel, Field


class LimitOffsetParams(BaseModel):
    """Pagination parameters based on limit-offset."""

    limit: int = Field(
        10,
        gt=0,
        le=100,
        description="Maximum number of records to return (between 1 and 100)",
    )
    offset: int = Field(0, ge=0, description="Number of records to skip")


class PaginatedLimitOffsetParams(LimitOffsetParams):
    """Extended limit-offset parameters with optional pagination toggle."""

    enable_pagination: bool = Field(True, description="Enable or disable pagination")
