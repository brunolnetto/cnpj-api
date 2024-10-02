from pydantic import BaseModel, Field

class LimitOffsetParams(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)


class PaginatedLimitOffsetParams(LimitOffsetParams):
    enable_pagination: bool = Field(True)
