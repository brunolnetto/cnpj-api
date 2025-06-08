from typing import Dict, List, Any
from datetime import datetime
import traceback
import asyncio
import inspect

from apscheduler import Scheduler, ScheduleLookupError
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.datastores.memory import MemoryDataStore

from backend.app.database.base import get_session
from backend.app.database.models.logs import TaskLog
from backend.app.api.models.tasks import TaskConfig, TaskCreate
from backend.app.api.repositories.tasks import TaskRepository
from backend.app.setup.config import settings
from backend.app.setup.logging import logger


class InvalidScheduleParameter(Exception):
    """Raised when invalid scheduling parameters are provided."""
    pass


def _validate_interval_kwargs(kwargs: Dict[str, Any]):
    allowed = {"weeks", "days", "hours", "minutes", "seconds", "start_date", "end_date", "timezone"}
    invalid = set(kwargs) - allowed
    if invalid:
        raise InvalidScheduleParameter(f"Invalid interval scheduling parameters: {invalid}")


def _validate_cron_kwargs(kwargs: Dict[str, Any]):
    allowed = {
        "year", "month", "day", "week", "day_of_week",
        "hour", "minute", "second", "start_date", "end_date",
        "timezone", "jitter"
    }
    invalid = set(kwargs) - allowed
    if invalid:
        raise InvalidScheduleParameter(f"Invalid cron scheduling parameters: {invalid}")


def create_scheduler(kind: str) -> Scheduler:
    """Creates a scheduler instance based on the type."""
    if kind == "background":
        return Scheduler(data_store=MemoryDataStore())
    raise ValueError(f"Unsupported scheduler type: {kind}")


class ScheduledTask:
    def __init__(self, task_config: TaskConfig):
        self.config = task_config

    def run(self):
        with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
            log = TaskLog(
                talo_task_id=self.config.task_id,
                talo_name=self.config.task_name,
                talo_type=self.config.task_type,
                talo_details=self.config.task_details,
                talo_start_time=datetime.now(),
                talo_status="running",
            )
            session.add(log)
            session.commit()

            try:
                if inspect.iscoroutinefunction(self.config.task_callable):
                    result = asyncio.run(
                        self.config.task_callable(*self.config.task_args, **self.config.task_details)
                    )
                else:
                    result = self.config.task_callable(*self.config.task_args, **self.config.task_details)

                log.talo_success = True
                log.talo_status = "success"
                log.talo_details["result"] = result

            except Exception as e:
                log.talo_success = False
                log.talo_status = "failed"
                log.talo_error_message = str(e)
                log.talo_error_trace = traceback.format_exc()

            finally:
                log.talo_end_time = datetime.now()
                session.commit()

    def get_trigger(self):
        params = self.config.schedule_params
        match self.config.task_type:
            case "interval":
                _validate_interval_kwargs(params)
                return IntervalTrigger(**params)
            case "cron":
                _validate_cron_kwargs(params)
                return CronTrigger(**params)
            case "date":
                if "run_time" not in params:
                    raise ValueError("Missing 'run_time' for 'date' task_type.")
                return DateTrigger(run_time=params["run_time"])
            case _:
                raise ValueError("Unsupported task_type. Use 'interval', 'cron' or 'date'.")


class TaskOrchestrator:
    def __init__(self):
        self.schedulers = {
            "background": create_scheduler("background")
        }

    async def start(self):
        self.schedulers["background"].start_in_background()

    async def shutdown(self):
        self.schedulers["background"].remove_schedule("")

    async def add_task(self, config: TaskConfig):
        scheduler = self._get_scheduler(config.schedule_type)
        task = ScheduledTask(config)
        scheduler.add_schedule(task.run, task.get_trigger(), id=str(task.config.task_id))

    def remove_task(self, schedule_type: str, task_id: str):
        scheduler = self._get_scheduler(schedule_type)
        try:
            scheduler.remove_schedule(task_id)
        except ScheduleLookupError:
            raise ValueError(f"Task '{task_id}' not found in scheduler '{schedule_type}'.")

    def list_tasks(self, schedule_type: str):
        return self._get_scheduler(schedule_type).get_jobs()

    async def remove_all_schedules(self):
        for scheduler in self.schedulers.values():
            scheduler.remove_schedule("")

    def remove_all_schedules_from(self, schedule_type: str):
        scheduler = self._get_scheduler(schedule_type)
        scheduler.remove_schedule()

    def _get_scheduler(self, schedule_type: str) -> Scheduler:
        scheduler = self.schedulers.get(schedule_type)
        if not scheduler:
            raise ValueError(
                f"Invalid scheduler type: {schedule_type}. "
                f"Available: {list(self.schedulers.keys())}"
            )
        return scheduler


class TaskRegister:
    def __init__(self, repository: TaskRepository):
        self.repo = repository

    def register(self, configs: List[TaskConfig]):
        for config in configs:
            data = TaskCreate(
                task_id=config.task_id,
                task_schedule_type=config.schedule_type,
                task_schedule_params=config.schedule_params,
                task_name=config.task_name,
                task_callable=config.task_callable.__name__,
                task_type=config.task_type,
                task_is_active=True,
                task_args=config.task_args,
                task_details=config.task_details,
            )
            try:
                self.repo.create(data.model_dump())
            except Exception as e:
                logger.error(f"Error registering task {data.task_name}: {e}")
