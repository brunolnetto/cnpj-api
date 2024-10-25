# app/schemas.py
from typing import Dict, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class RequestLogBase(BaseModel):
    """Base model for request logs."""

    relo_method: str = Field(
        ..., description="HTTP method used for the request", min_length=1
    )
    relo_url: str = Field(..., description="URL of the request")
    relo_body: Optional[str] = Field(None, description="Request body content")
    relo_headers: Dict[str, str] = Field(..., description="Request headers")
    relo_status_code: int = Field(
        ..., description="HTTP status code of the response", ge=100, le=599
    )
    relo_ip_address: Optional[str] = Field(
        None, description="Client's IP address")
    relo_device_info: Optional[str] = Field(
        None, description="Information about the client device"
    )
    relo_absolute_path: Optional[str] = Field(
        None, description="Absolute path of the request"
    )
    relo_request_duration_seconds: Optional[float] = Field(
        None, ge=0, description="Duration of the request in seconds"
    )
    relo_response_size: Optional[int] = Field(
        None, ge=0, description="Size of the response in bytes"
    )


class RequestLogCreate(RequestLogBase):
    """Schema for creating a new request log."""

    pass


class TaskLogCreate(BaseModel):
    """Schema for creating a new task log."""

    talo_name: str = Field(..., description="Name of the task")
    talo_status: str = Field(
        ..., description="Current status of the task", min_length=1
    )
    talo_type: str = Field(..., description="Type of the task", min_length=1)
    talo_details: Dict[str, Optional[str]] = Field(
        default_factory=dict, description="Detailed information about the task"
    )
    talo_start_time: datetime = Field(...,
                                      description="Start time of the task")
    talo_end_time: Optional[datetime] = Field(
        None, description="End time of the task")
    talo_success: bool = Field(
        False, description="Indicates whether the task was successful"
    )
    talo_error_message: Optional[str] = Field(
        None, description="Error message if the task failed"
    )
    talo_error_trace: Optional[str] = Field(
        None, description="Error traceback details if the task failed"
    )
