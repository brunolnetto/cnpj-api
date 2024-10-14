from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.app.setup.config import settings
from backend.app.database.base import get_session
from backend.app.api.repositories.logs import RequestLogRepository, TaskLogRepository

AuditSessionDependency=Annotated[
    AsyncSession, Depends(lambda: get_session(settings.POSTGRES_DBNAME_AUDIT))
]

def get_request_logs_repository():
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return RequestLogRepository(session)


def get_task_logs_repository():
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return TaskLogRepository(session)

TaskLogsRepositoryDependency = Depends(get_task_logs_repository)
RequestLogsRepositoryDependency = Depends(get_request_logs_repository)

