# app/repositories/request_log_repository.py
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

from uuid import UUID
from ipwhois import IPWhois
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from backend.app.setup.config import settings
from backend.app.database.models.logs import DebugLog
from backend.app.database.models.logs import TaskLog, RequestLog, AppStartLog
from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.base import BaseRepository
from backend.app.api.models.logs import TaskLogCreate


class RequestLogRepository(BaseRepository):
    def create(self, log: RequestLogCreate) -> RequestLog:
        db_log = RequestLog(**log.model_dump())
        self.session.add(db_log)
        self.session.commit()
        self.session.refresh(db_log)
        return db_log

    def update(self, item_id: UUID, data: Dict[str, Any]) -> Optional[RequestLog]:
        # Not typically used for RequestLog, but implemented for completeness
        return None

    def get_by_id(self, item_id: UUID) -> Optional[RequestLog]:
        return self.session.get(RequestLog, item_id)

    def delete_by_id(self, item_id: UUID) -> bool:
        log = self.get_by_id(item_id)
        if not log:
            return False
        self.session.delete(log)
        self.session.commit()
        return True

    def get_all(self, limit: int = 100, offset: int = 0) -> List[RequestLog]:
        result = self.session.execute(select(RequestLog).offset(offset).limit(limit))
        return result.scalars().all()

    def delete_old_logs(self, time_delta: timedelta):
        cutoff_date = datetime.now() - time_delta
        delete_query = delete(RequestLog).where(
            RequestLog.relo_inserted_at < cutoff_date
        )
        self.session.execute(delete_query)
        self.session.commit()

    def delete_excess_logs(self, max_rows: int):
        query = self.session.query(RequestLog).order_by(RequestLog.relo_inserted_at)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = query.delete(synchronize_session="fetch")
            self.session.execute(delete_query)
            self.session.commit()

    def lookup_and_update_ip_info(self):
        # Get all logs with missing IP info
        logs_without_ip_info = (
            self.session.query(RequestLog).filter(RequestLog.relo_ip_info == {}).all()
        )

        for log in logs_without_ip_info:
            ip_address = log.relo_ip_address
            if ip_address:
                try:
                    # Perform IP lookup
                    obj = IPWhois(ip_address)
                    results = obj.lookup_rdap(depth=1)

                    # Update the log's IP info
                    self.session.query(RequestLog).filter(
                        RequestLog.relo_id == log.relo_id
                    ).update({RequestLog.relo_ip_info: results})
                    self.session.commit()
                except Exception as e:
                    print(f"Error looking up IP {ip_address}: {e}")
                    self.session.rollback()


class TaskLogRepository(BaseRepository):
    def create(self, task_log_data: TaskLogCreate) -> TaskLog:
        task_log = TaskLog(**task_log_data)
        self.session.add(task_log)
        self.session.commit()
        self.session.refresh(task_log)
        return task_log

    def update(self, item_id: UUID, data: TaskLogCreate) -> Optional[TaskLog]:
        task_log = self.get_by_id(item_id)
        if not task_log:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task_log, key, value)

        self.session.commit()
        self.session.refresh(task_log)
        return task_log

    def get_by_id(self, item_id: UUID) -> Optional[TaskLog]:
        return self.session.get(TaskLog, item_id)

    def delete_by_id(self, item_id: UUID) -> bool:
        task_log = self.get_by_id(item_id)
        if not task_log:
            return False

        self.session.delete(task_log)
        self.session.commit()
        return True

    def get_all(self, limit: int = 100, offset: int = 0) -> List[TaskLog]:
        return (
            self.session.execute(select(TaskLog).offset(offset).limit(limit))
            .scalars()
            .all()
        )

    def delete_old_logs(self, time_delta: timedelta):
        cutoff_date = datetime.now() - time_delta
        self.session.query(TaskLog).filter(
            TaskLog.talo_start_time < cutoff_date
        ).delete()
        self.session.commit()

    def delete_excess_logs(self, max_rows: int):
        query = self.session.query(TaskLog).order_by(TaskLog.talo_inserted_at)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = query.delete(synchronize_session="fetch")
            self.session.execute(delete_query)
            self.session.commit()


class AppStartLogRepository(BaseRepository):
    def create(self, log_data: Dict[str, Any]) -> AppStartLog:
        """
        Creates a new AppStartLog entry in the database.
        """
        app_start_log = AppStartLog(**log_data)
        self.session.add(app_start_log)
        self.session.commit()
        self.session.refresh(app_start_log)
        return app_start_log

    def get_by_id(self, item_id: UUID) -> Optional[AppStartLog]:
        """
        Retrieves an AppStartLog entry by its ID.
        """
        return self.session.get(AppStartLog, item_id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[AppStartLog]:
        """
        Retrieves all AppStartLog entries with pagination support.
        """
        result = self.session.execute(select(AppStartLog).offset(offset).limit(limit))
        return result.scalars().all()

    def delete_by_id(self, item_id: UUID) -> bool:
        """
        Deletes an AppStartLog entry by its ID.
        """
        app_start_log = self.get_by_id(item_id)
        if not app_start_log:
            return False
        self.session.delete(app_start_log)
        self.session.commit()
        return True

    def delete_old_logs(self, time_delta: timedelta):
        """
        Deletes AppStartLog entries older than a specified time delta.
        """
        cutoff_date = datetime.now() - time_delta
        self.session.query(AppStartLog).filter(
            AppStartLog.stlo_start_time < cutoff_date
        ).delete()
        self.session.commit()

    def delete_excess_logs(self, max_rows: int):
        """
        Deletes excess AppStartLog entries, keeping only a specified number of rows.
        """
        query = self.session.query(AppStartLog).order_by(AppStartLog.stlo_start_time)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = query.delete(synchronize_session="fetch")
            self.session.execute(delete_query)
            self.session.commit()


class DebuggingDatabaseHandler(logging.Handler):
    """
    A custom logging handler that logs messages to the database.
    """

    def __init__(self, db_session: Session):
        logging.Handler.__init__(self)
        self.session = db_session

    def emit(self, record):
        # This is where you format the log record
        log_entry = self.format(record)

        # Create a new DebugLog entry and add it to the session
        debug_log = DebugLog(
            delo_created_at=datetime.fromtimestamp(record.created),
            delo_level=record.levelname,
            delo_message=log_entry,
            delo_pathname=record.pathname,
            delo_func_name=record.funcName,
            delo_lineno=record.lineno,
            delo_environment=settings.ENVIRONMENT,
            delo_machine=settings.MACHINE_NAME,
        )

        # Add the log to the database and commit the session
        self.session.add(debug_log)
        self.session.commit()

    def delete_old_logs(self, time_delta: timedelta):
        """
        Deletes DebugLog entries older than a specified time delta.
        """
        cutoff_date = datetime.now() - time_delta
        self.session.query(DebugLog).filter(
            DebugLog.delo_created_at < cutoff_date
        ).delete()
        self.session.commit()

    def delete_excess_logs(self, max_rows: int):
        """
        Deletes excess AppStartLog entries, keeping only a specified number of rows.
        """
        query = self.session.query(DebugLog).order_by(DebugLog.delo_created_at)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = query.delete(synchronize_session="fetch")
            self.session.execute(delete_query)
            self.session.commit()
