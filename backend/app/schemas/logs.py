# app/schemas.py
from pydantic import BaseModel, Field, UUID4
from typing import List, Dict, Callable, Optional, Any
from datetime import datetime
from uuid import uuid4


class RequestLogBase(BaseModel):
    relo_method: str
    relo_url: str
    relo_body: Optional[str] = None
    relo_headers: dict
    relo_status_code: int
    relo_ip_address: Optional[str] = Field(None, description="Client's IP address")
    relo_device_info: Optional[str] = Field(None, description="Device information")
    relo_absolute_path: Optional[str] = Field(
        None, description="Absolute path of the request"
    )
    relo_request_duration_seconds: Optional[float] = Field(
        None, description="Duration of the request in seconds"
    )
    relo_response_size: Optional[int] = Field(
        None, description="Size of the response in bytes"
    )


class RequestLogCreate(RequestLogBase):
    pass