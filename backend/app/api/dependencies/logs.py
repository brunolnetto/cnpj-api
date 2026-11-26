from datetime import datetime
from typing import Iterator

from fastapi import Depends

from backend.app.setup.config import settings
from backend.app.database.base import get_session
from backend.app.api.repositories.logs import (
    RequestLogRepository,
    TaskLogRepository,
    AppStartLogRepository,
)
from backend.app.api.repositories.logs import DebuggingDatabaseHandler
from backend.app.database.base import multi_database


def get_debug_logs_handler():
    audit_database = multi_database.databases[settings.POSTGRES_DBNAME_AUDIT]
    session = audit_database.session_maker()

    # Create the database handler
    return DebuggingDatabaseHandler(db_session=session)


def get_request_logs_repository() -> Iterator[RequestLogRepository]:
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        yield RequestLogRepository(session)


def get_task_logs_repository() -> Iterator[TaskLogRepository]:
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        yield TaskLogRepository(session)


def get_app_start_logs_repository() -> Iterator[AppStartLogRepository]:
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        yield AppStartLogRepository(session)


def log_app_start():
    app_start_log = {"stlo_start_time": datetime.now()}

    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        AppStartLogRepository(session).create(app_start_log)


TaskLogsRepositoryDependency = Depends(get_task_logs_repository)
RequestLogsRepositoryDependency = Depends(get_request_logs_repository)
