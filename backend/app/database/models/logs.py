
import uuid

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

logs_database=multi_database.databases[settings.POSTGRES_DBNAME_AUDIT]

class RequestLog(logs_database.base):
    __tablename__ = "request_logs"

    relo_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    relo_inserted_at = Column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )
    relo_method = Column(String, index=True)
    relo_url = Column(String, index=True)
    relo_headers = Column(JSONB)
    relo_body = Column(String)
    relo_status_code = Column(Integer, index=True)
    relo_ip_address = Column(String, index=True)
    relo_device_info = Column(String)
    relo_absolute_path = Column(String)
    relo_request_duration_seconds = Column(Integer, index=True)
    relo_response_size = Column(Integer, index=True)

    def __repr__(self):
        params = f"id={self.relo_id}, method={self.relo_method}, url={self.relo_url}, status_code={self.relo_status_code}"
        return f"<RequestLog({params})>"
