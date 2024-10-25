import uuid

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    Float,
    DateTime,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

logs_database = multi_database.databases[settings.POSTGRES_DBNAME_AUDIT]


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
    relo_ip_address = Column(JSONB, index=True)
    relo_ip_info = Column(JSONB, default={})
    relo_device_info = Column(String)
    relo_absolute_path = Column(String)
    relo_request_duration_seconds = Column(Float, index=True)
    relo_response_size = Column(Integer, index=True)

    def __repr__(self):
        params = f"id={self.relo_id}, method={self.relo_method}, url={self.relo_url}, status_code={self.relo_status_code}"
        return f"<RequestLog({params})>"


class Task(logs_database.base):
    __tablename__ = "my_tasks"
    task_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    task_created_at = Column(
        DateTime(
            timezone=True),
        server_default=func.now())
    task_schedule_type = Column(String, index=True)
    task_schedule_params = Column(JSONB)
    task_name = Column(String, index=True)
    task_callable = Column(String, index=True)
    task_type = Column(String)
    task_is_active = Column(Boolean, default=True)

    # Define a relationship with TaskLog model (one-to-many)
    logs = relationship(
        "TaskLog",
        back_populates="task",
        cascade="all, delete",
        passive_updates=False)

    def __repr__(self):
        params = f"id={self.task_id}, name={self.task_name}, type={self.task_type}, active={self.task_is_active}"
        return f"<Task({params})>"


class TaskLog(logs_database.base):
    __tablename__ = "task_logs"

    talo_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )

    # Foreign key referencing the task_id in Task
    talo_task_id = Column(
        UUID(as_uuid=True),
        ForeignKey("my_tasks.task_id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
        nullable=False,
    )

    talo_name = Column(String, index=True)
    talo_status = Column(String, index=True)
    talo_type = Column(String)
    talo_details = Column(JSONB)
    talo_start_time = Column(DateTime(timezone=True), index=True)
    talo_end_time = Column(DateTime(timezone=True), index=True)
    talo_success = Column(Boolean, default=False)
    talo_error_message = Column(Text, nullable=True)
    talo_error_trace = Column(Text, nullable=True)
    talo_inserted_at = Column(
        DateTime(
            timezone=True),
        server_default=func.now())

    task = relationship("Task", back_populates="logs")

    def __repr__(self):
        params = f"id={self.talo_id}, name={self.talo_name}, status={self.talo_status}, success={self.talo_success}"
        return f"<TaskLog({params})>"


class AppStartLog(logs_database.base):
    __tablename__ = "startup_logs"

    stlo_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    stlo_start_time = Column(
        DateTime(
            timezone=True),
        server_default=func.now())

    def __repr__(self):
        params = f"id={self.stlo_id}, time={self.stlo_start_time}"
        return f"<AppRestartLog({params})>"


class DebugLog(logs_database.base):
    __tablename__ = "debug_logs"

    delo_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    delo_created_at = Column(
        DateTime(
            timezone=True),
        server_default=func.now())
    delo_environment = Column(String)
    delo_machine = Column(String)
    delo_level = Column(String, index=True)
    delo_message = Column(String)
    delo_pathname = Column(String)
    delo_func_name = Column(String)
    delo_lineno = Column(Integer)


class RequestTimingLog(logs_database.base):
    __tablename__ = "request_timing"

    rtlo_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    rtlo_created_at = Column(
        DateTime(
            timezone=True),
        server_default=func.now())
    rtlo_url_path = Column(String, index=True)
    rtlo_method = Column(String)
    rtlo_process_time = Column(Float)
