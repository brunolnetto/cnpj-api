# app/schemas.py
from typing import Dict, Optional
from datetime import datetime

from pydantic import BaseModel, Field


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


class TaskLogCreate(BaseModel):
    talo_name: str
    talo_status: str
    talo_type: str
    talo_details: Dict[str, Optional[str]] = Field(default_factory=dict)
    talo_start_time: datetime
    talo_end_time: Optional[datetime] = None
    talo_success: bool = False
    talo_error_message: Optional[str] = None
    talo_error_trace: Optional[str] = None
