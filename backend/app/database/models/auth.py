import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

auth_database = multi_database.databases[settings.POSTGRES_DBNAME_AUDIT]


class ApiClient(auth_database.base):
    """A consumer of the API, authenticated with client credentials."""

    __tablename__ = "api_clients"

    apcl_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apcl_client_id = Column(String, unique=True, index=True, nullable=False)
    apcl_name = Column(String, nullable=False)
    apcl_secret_hash = Column(String, nullable=False)
    apcl_is_active = Column(Boolean, nullable=False, default=True)
    apcl_created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<ApiClient(client_id={self.apcl_client_id}, name={self.apcl_name}, "
            f"active={self.apcl_is_active})>"
        )
