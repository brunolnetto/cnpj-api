# app/repositories/request_log_repository.py
from datetime import datetime, timedelta
from sqlalchemy import delete
from sqlalchemy.future import select
from typing import Dict, Any, List, Optional

from uuid import UUID

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

    def update(self, id: UUID, data: Dict[str, Any]) -> Optional[RequestLog]:
        # Not typically used for RequestLog, but implemented for completeness
        return None

    def get_by_id(self, id: UUID) -> Optional[RequestLog]:
        return self.session.get(RequestLog, id)

    def delete_by_id(self, id: UUID) -> bool:
        log = self.get_by_id(id)
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


class RequestLogRepository(BaseRepository):
    def create(self, log: RequestLogCreate) -> RequestLog:
        db_log = RequestLog(**log.model_dump())
        self.session.add(db_log)
        self.session.commit()
        self.session.refresh(db_log)
        return db_log

    def update(self, id: UUID, data: Dict[str, Any]) -> Optional[RequestLog]:
        # Not typically used for RequestLog, but implemented for completeness
        return None

    def get_by_id(self, id: UUID) -> Optional[RequestLog]:
        return self.session.get(RequestLog, id)

    def delete_by_id(self, id: UUID) -> bool:
        log = self.get_by_id(id)
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

class TaskLogRepository(BaseRepository):
    def create(self, task_log_data: TaskLogCreate) -> TaskLog:
        task_log = TaskLog(**task_log_data)
        self.session.add(task_log)
        self.session.commit()
        self.session.refresh(task_log)
        return task_log

    def update(self, id: UUID, data: TaskLogCreate) -> Optional[TaskLog]:
        task_log = self.get_by_id(id)
        if not task_log:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task_log, key, value)

        self.session.commit()
        self.session.refresh(task_log)
        return task_log

    def get_by_id(self, id: UUID) -> Optional[TaskLog]:
        return self.session.get(TaskLog, id)

    def delete_by_id(self, id: UUID) -> bool:
        task_log = self.get_by_id(id)
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

    def get_by_id(self, id: UUID) -> Optional[AppStartLog]:
        """
        Retrieves an AppStartLog entry by its ID.
        """
        return self.session.get(AppStartLog, id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[AppStartLog]:
        """
        Retrieves all AppStartLog entries with pagination support.
        """
        result = self.session.execute(select(AppStartLog).offset(offset).limit(limit))
        return result.scalars().all()

    def delete_by_id(self, id: UUID) -> bool:
        """
        Deletes an AppStartLog entry by its ID.
        """
        app_start_log = self.get_by_id(id)
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
        self.session.query(AppStartLog).filter(AppStartLog.restart_time < cutoff_date).delete()
        self.session.commit()

    def delete_excess_logs(self, max_rows: int):
        """
        Deletes excess AppStartLog entries, keeping only a specified number of rows.
        """
        query = self.session.query(AppStartLog).order_by(AppStartLog.restart_time)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = query.delete(synchronize_session="fetch")
            self.session.execute(delete_query)
            self.session.commit()
