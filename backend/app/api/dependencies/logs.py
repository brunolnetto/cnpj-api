from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.setup.config import settings
from backend.app.database.base import get_session
from backend.app.api.repositories.logs import (
    RequestLogRepository, 
    TaskLogRepository, 
    AppStartLogRepository,
)

def get_request_logs_repository():
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return RequestLogRepository(session)


def get_task_logs_repository():
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return TaskLogRepository(session)

def get_app_start_logs_repository():
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return AppStartLogRepository(session)

TaskLogsRepositoryDependency = Depends(get_task_logs_repository)
RequestLogsRepositoryDependency = Depends(get_request_logs_repository)
AppStartLogRepositoryDependency = Depends(get_app_start_logs_repository)

