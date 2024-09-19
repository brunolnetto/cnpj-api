# app/repositories/request_log_repository.py
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
import asyncio
from datetime import datetime


from uuid import UUID
from ipwhois import IPWhois
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.setup.config import settings
from backend.app.database.models.logs import DebugLog
from backend.app.database.models.logs import TaskLog, RequestLog, AppStartLog
from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.base import BaseRepository
from backend.app.api.models.logs import TaskLogCreate


class RequestLogRepository(BaseRepository):
    async def create(self, data: RequestLogCreate) -> RequestLog:
        db_log = RequestLog(**data.model_dump())
        await self.session.add(db_log)
        await self.session.commit()
        await self.session.refresh(db_log)
        return db_log

    async def update(self, item_id: UUID, data: Dict[str, Any]) -> Optional[RequestLog]:
        # Not typically used for RequestLog, but implemented for completeness
        return None

    async def get_by_id(self, item_id: UUID) -> Optional[RequestLog]:
        return await self.session.get(RequestLog, item_id)

    async def delete_by_id(self, item_id: UUID) -> bool:
        log = self.get_by_id(item_id)
        if not log:
            return False
        self.session.delete(log)
        self.session.commit()
        return True

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[RequestLog]:
        result = await self.session.execute(select(RequestLog).offset(offset).limit(limit))
        return result.scalars().all()

    async def delete_old_logs(self, time_delta: timedelta):
        cutoff_date = datetime.now() - time_delta
        delete_query = await delete(RequestLog).where(
            RequestLog.relo_inserted_at < cutoff_date
        )
        await self.session.execute(delete_query)
        await self.session.commit()

    async def delete_excess_logs(self, max_rows: int):
        query = await self.session.query(RequestLog).order_by(RequestLog.relo_inserted_at)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = await query.delete(synchronize_session="fetch")
            await self.session.execute(delete_query)
            await self.session.commit()
    
    async def lookup_and_update_ip_info(self):
        # Get all logs with missing IP info
        logs_without_ip_info = (
            await self.session.query(RequestLog).filter(RequestLog.relo_ip_info == {}).all()
        )

        for log in logs_without_ip_info:
            ip_address = log.relo_ip_address
            if ip_address:
                try:
                    # Convert the IP address to an ip_address object
                    ip_obj = ip_address.ip_address(ip_address)
                    
                    # Check if the IP is public
                    if not (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved):
                        # Perform IP lookup only for public IPs
                        obj = IPWhois(ip_address)
                        results = obj.lookup_rdap(depth=1)

                        # Update the log's IP info
                        await self.session.query(RequestLog).filter(
                            RequestLog.relo_id == log.relo_id
                        ).update({RequestLog.relo_ip_info: results})
                        await self.session.commit()
                    else:
                        print(f"Skipping local or inappropriate IP: {ip_address}")

                except Exception as e:
                    print(f"Error looking up IP {ip_address}: {e}")
                    await self.session.rollback()


class TaskLogRepository(BaseRepository):
    async def create(self, data: TaskLogCreate) -> TaskLog:
        task_log = TaskLog(**data)
        await self.session.add(task_log)
        await self.session.commit()
        await self.session.refresh(task_log)
        return task_log

    async def update(self, item_id: UUID, data: TaskLogCreate) -> Optional[TaskLog]:
        task_log = self.get_by_id(item_id)
        if not task_log:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task_log, key, value)

        await self.session.commit()
        await self.session.refresh(task_log)
        return task_log

    async def get_by_id(self, item_id: UUID) -> Optional[TaskLog]:
        return await self.session.get(TaskLog, item_id)

    async def delete_by_id(self, item_id: UUID) -> bool:
        task_log = await self.get_by_id(item_id)
        if not task_log:
            return False

        self.session.delete(task_log)
        self.session.commit()
        return True

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[TaskLog]:
        return (
            await self.session.execute(select(TaskLog).offset(offset).limit(limit))
            .scalars()
            .all()
        )

    async def delete_old_logs(self, time_delta: timedelta):
        cutoff_date = datetime.now() - time_delta
        await self.session.query(TaskLog).filter(
            TaskLog.talo_start_time < cutoff_date
        ).delete()
        await self.session.commit()

    async def delete_excess_logs(self, max_rows: int):
        query = await self.session.query(TaskLog).order_by(TaskLog.talo_inserted_at)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = await query.delete(synchronize_session="fetch")
            await self.session.execute(delete_query)
            await self.session.commit()


class AppStartLogRepository(BaseRepository):
    async def create(self, data: Dict[str, Any]) -> AppStartLog:
        """
        Creates a new AppStartLog entry in the database.
        """
        app_start_log = AppStartLog(**data)
        self.session.add(app_start_log)
        await self.session.commit()
        await self.session.refresh(app_start_log)
        return app_start_log

    async def get_by_id(self, item_id: UUID) -> Optional[AppStartLog]:
        """
        Retrieves an AppStartLog entry by its ID.
        """
        return await self.session.get(AppStartLog, item_id)

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[AppStartLog]:
        """
        Retrieves all AppStartLog entries with pagination support.
        """
        result = await self.session.execute(select(AppStartLog).offset(offset).limit(limit))
        return result.scalars().all()

    async def delete_by_id(self, item_id: UUID) -> bool:
        """
        Deletes an AppStartLog entry by its ID.
        """
        app_start_log = self.get_by_id(item_id)
        if not app_start_log:
            return False
        await self.session.delete(app_start_log)
        await self.session.commit()
        return True

    async def delete_old_logs(self, time_delta: timedelta):
        """
        Deletes AppStartLog entries older than a specified time delta.
        """
        cutoff_date = datetime.now() - time_delta
        await self.session.query(AppStartLog).filter(
            AppStartLog.stlo_start_time < cutoff_date
        ).delete()
        await self.session.commit()

    async def delete_excess_logs(self, max_rows: int):
        """
        Deletes excess AppStartLog entries, keeping only a specified number of rows.
        """
        query = await self.session.query(AppStartLog).order_by(AppStartLog.stlo_start_time)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = await query.delete(synchronize_session="fetch")
            await self.session.execute(delete_query)
            await self.session.commit()


class DebuggingDatabaseHandler(logging.Handler):
    """
    A custom logging handler that logs messages to the database.
    """

    def __init__(self, db_session: Session):
        logging.Handler.__init__(self)
        self.session = db_session
        self.queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.stop_event = asyncio.Event()
        self.loop.create_task(self.process_queue())

    def emit(self, record):
        # This is where you format the log record
        log_entry = self.format(record)

        # Create a new DebugLog entry and add it to the session
        log_data = {
            "created_at": datetime.fromtimestamp(record.created),
            "level": record.levelname,
            "message": log_entry,
            "pathname": record.pathname,
            "func_name": record.funcName,
            "lineno": record.lineno,
            "environment": settings.ENVIRONMENT,
            "machine_name": settings.MACHINE_NAME,
        }

        # Add the log to the database and commit the session
        self.queue.put_nowait(log_data)
    
    async def process_queue(self):
        while not self.stop_event.is_set() or not self.queue.empty():
            log_data = await self.queue.get()
            await self.write_to_db(log_data)
            self.queue.task_done()
            
    async def write_to_db(self, log_data):
        # Create a new DebugLog entry and add it to the session
        debug_log = DebugLog(
            delo_created_at=log_data["created_at"],
            delo_level=log_data["level"],
            delo_message=log_data["message"],
            delo_pathname=log_data["pathname"],
            delo_func_name=log_data["func_name"],
            delo_lineno=log_data["lineno"],
            delo_environment=log_data["environment"],
            delo_machine=log_data["machine_name"],
        )

        # Add the log to the database and commit the session
        self.session.add(debug_log)
        await self.session.commit()

    def close(self):
        self.stop_event.set()
        self.loop.run_until_complete(self.queue.join())
        super().close()

    async def delete_old_logs(self, time_delta: timedelta):
        """
        Deletes DebugLog entries older than a specified time delta.
        """
        cutoff_date = datetime.now() - time_delta
        await self.session.query(DebugLog).filter(
            DebugLog.delo_created_at < cutoff_date
        ).delete()
        await self.session.commit()

    async def delete_excess_logs(self, max_rows: int):
        """
        Deletes excess AppStartLog entries, keeping only a specified number of rows.
        """
        query = await self.session.query(DebugLog).order_by(DebugLog.delo_created_at)
        total_rows = query.count()
        if total_rows > max_rows:
            delete_query = await query.delete(synchronize_session="fetch")
            await self.session.execute(delete_query)
            await self.session.commit()
