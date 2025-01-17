from datetime import timedelta

from backend.app.database.base import get_session
from backend.app.api.repositories.logs import (
    RequestLogRepository,
    TaskLogRepository,
    DebuggingDatabaseHandler,
)
from backend.app.api.models.tasks import TaskConfig
from backend.app.setup.config import settings


def cleanup_request_logs(time_delta: timedelta, max_rows: int = None):
    """
    Cleans up requests logs based on either time or table row count.

    Args:
        time_delta (timedelta): The time difference from now. Logs older than
        this will be deleted.
        max_rows (int, optional): The maximum number of rows to retain. If specified,
        logs will be deleted based on their creation time and this count.
    """
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        request_log_repository = RequestLogRepository(db_session)
        if max_rows is not None:
            request_log_repository.delete_excess_logs(max_rows)
        else:
            request_log_repository.delete_old_logs(time_delta)


def lookup_and_update_ip_info_task():
    """
    Cleans up requests logs based on either time or table row count.

    Args:
        time_delta (timedelta): The time difference from now. Logs older than this
        will be deleted.
        max_rows (int, optional): The maximum number of rows to retain. If specified,
        logs will be deleted based on their creation time and this count.
    """
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        request_log_repository = RequestLogRepository(db_session)
        request_log_repository.lookup_and_update_ip_info()


def cleanup_task_logs(time_delta: timedelta, max_rows: int = None):
    """
    Cleans up tasks logs based on either time or table row count.

    Args:
        time_delta (timedelta): The time difference from now. Logs older than this
        will be deleted.
        max_rows (int, optional): The maximum number of rows to retain. If specified,
        logs will be deleted based on their creation time and this count.
    """
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        task_log_repository = TaskLogRepository(db_session)
        if max_rows is not None:
            task_log_repository.delete_excess_logs(max_rows)
        else:
            task_log_repository.delete_old_logs(time_delta)


def cleanup_debug_logs(time_delta: timedelta, max_rows: int = None):
    """
    Cleans up tasks logs based on either time or table row count.

    Args:
        time_delta (timedelta): The time difference from now. Logs older than
        this will be deleted.
        max_rows (int, optional): The maximum number of rows to retain. If specified,
        logs will be deleted based on their creation time and this count.
    """
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        debug_log_repository = DebuggingDatabaseHandler(db_session)
        if max_rows is not None:
            debug_log_repository.delete_excess_logs(max_rows)
        else:
            debug_log_repository.delete_old_logs(time_delta)


# Schedule the task to run at regular intervals
cleanup_request_config = TaskConfig(
    schedule_type="background",
    schedule_params=settings.CLEANUP_CRON_KWARGS,
    task_name="Cleanup request logs",
    task_type="cron",
    task_callable=cleanup_request_logs,
    task_args=[
        settings.REQUEST_CLEANUP_AGE,
        settings.CLEANUP_MAX_ROWS,
    ],
)

# Schedule the task to run at regular intervals
cleanup_task_config = TaskConfig(
    schedule_type="background",
    schedule_params=settings.CLEANUP_CRON_KWARGS,
    task_name="Cleanup task logs",
    task_type="cron",
    task_callable=cleanup_task_logs,
    task_args=[
        settings.REQUEST_CLEANUP_AGE,
        settings.CLEANUP_MAX_ROWS,
    ],
)

# Schedule the task to run at regular intervals
cleanup_debug_config = TaskConfig(
    schedule_type="background",
    schedule_params=settings.CLEANUP_CRON_KWARGS,
    task_name="Cleanup debug logs",
    task_type="cron",
    task_callable=cleanup_debug_logs,
    task_args=[
        settings.DEBUG_CLEANUP_AGE,
        settings.CLEANUP_MAX_ROWS,
    ],
)

# Augment IPs with metadata
lookup_and_update_ip_info_config = TaskConfig(
    schedule_type="background",
    schedule_params=settings.IP_LOOKUP_CRON_KWARGS,
    task_name="Augment IPs with metadata",
    task_type="cron",
    task_callable=lookup_and_update_ip_info_task,
)
