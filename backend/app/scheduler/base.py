from typing import Dict, List, Any
from datetime import datetime
from copy import deepcopy
import traceback
from copy import deepcopy
import asyncio
import inspect

from apscheduler import Scheduler, ScheduleLookupError
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

from backend.app.database.base import multi_database
from backend.app.database.base import get_session
from backend.app.setup.logging import logger
from backend.app.database.models.logs import TaskLog
from backend.app.api.models.tasks import TaskConfig, TaskCreate
from backend.app.api.repositories.tasks import TaskRepository
from backend.app.setup.config import settings

# Custom exception for invalid scheduling parameters


class InvalidScheduleParameter(Exception):
    pass


def validate_date_format(date_str: str, date_format: str = "%Y-%m-%d"):
    try:
        datetime.strptime(date_str, date_format)
    except ValueError:
        raise InvalidScheduleParameter(
            f"Date '{date_str}' does not match format '{date_format}'"
        )


def validate_interval_kwargs(kwargs: Dict[str, Any]):
    allowed_keys = {
        "weeks",
        "days",
        "hours",
        "minutes",
        "seconds",
        "start_date",
        "end_date",
        "timezone",
    }
    invalid_keys = set(kwargs) - allowed_keys
    if invalid_keys:
        raise InvalidScheduleParameter(
            f"Invalid interval scheduling parameters: {invalid_keys}"
        )


def validate_cron_kwargs(kwargs: Dict[str, Any]):
    allowed_keys = {
        "year",
        "month",
        "day",
        "week",
        "day_of_week",
        "hour",
        "minute",
        "second",
        "start_date",
        "end_date",
        "timezone",
        "jitter",
    }
    invalid_keys = set(kwargs) - allowed_keys
    if invalid_keys:
        raise InvalidScheduleParameter(
            f"Invalid cron scheduling parameters: {invalid_keys}"
        )


# Define a function to create the appropriate scheduler
audit_database = multi_database.databases[settings.POSTGRES_DBNAME_AUDIT]


def create_scheduler(schedule_type):
    datastore = SQLAlchemyDataStore(engine_or_url=audit_database.engine)

    if schedule_type == "background":
        return Scheduler(data_store=datastore)
    else:
        raise ValueError(f"Unsupported scheduler type: {schedule_type}")


class ScheduledTask:
    def __init__(self, task_config: TaskConfig):
        self.task_config = task_config

    def run(self):
        """
        Run a task and log its execution details in the TaskLog table.

        Args:
            task_name (str): The name of the task being executed.
            task_type (str): The type of task (e.g., 'cleanup', 'data_processing').
            task_details (Dict[str, Any]): Additional details about the task (e.g., parameters used).
            task_callable (Callable): The function or method that executes the task logic.
            *args: Positional arguments to pass to the task_callable.
            **kwargs: Keyword  arguments to pass to the task_callable.
        """
        with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
            task_log = TaskLog(
                talo_task_id=self.task_config.task_id,
                talo_name=self.task_config.task_name,
                talo_type=self.task_config.task_type,
                talo_details=self.task_config.task_details,
                talo_start_time=datetime.now(),
                talo_status="running",
            )
            session.add(task_log)
            session.commit()

            try:
                if inspect.iscoroutinefunction(self.task_config.task_callable):
                    result = asyncio.run(
                        self.task_config.task_callable(
                            *self.task_config.task_args, **self.task_config.task_details
                        )
                    )
                else:
                    result = self.task_config.task_callable(
                        *self.task_config.task_args, **self.task_config.task_details
                    )

                task_log.talo_success = True
                task_log.talo_status = "success"
                task_log.talo_details["result"] = result

            except Exception as e:
                task_log.talo_success = False
                task_log.talo_status = "failed"
                task_log.talo_error_message = str(e)
                task_log.talo_error_trace = traceback.format_exc()

            finally:
                task_log.talo_end_time = datetime.now()
                session.commit()

    # Generic function to set up scheduler
    def get_scheduler_trigger(self):
        """
        Set up the scheduler to run a specified job function based on the given schedule type.

        Args:
            job_function (callable): The function to schedule.
            schedule_type (str): The type of schedule to use ('interval' or 'cron').
            **kwargs: Additional keyword arguments for the trigger, such as 'days', 'hours', 'cron' parameters, etc.
        """
        task_type = self.task_config.task_type
        schedule_params = self.task_config.schedule_params

        if task_type == "interval":
            validate_interval_kwargs(schedule_params)
            trigger = IntervalTrigger(**schedule_params)
        elif task_type == "cron":
            validate_cron_kwargs(schedule_params)
            trigger = CronTrigger(**schedule_params)
        elif task_type == "date":
            if "run_time" not in schedule_params:
                message = "For task_type 'date', 'run_time' must be specified in schedule_params."
                raise ValueError(message)
            trigger = DateTrigger(
                run_time=schedule_params["run_time"]
            )
        else:
            raise ValueError(
                "Unsupported schedule_type. Use 'interval', 'cron' or 'date'."
            )

        return trigger

    def schedule(self, scheduler: Scheduler):
        trigger = self.get_scheduler_trigger()
        id_=str(self.task_config.task_id)
        scheduler.add_schedule(self.run, trigger, id=id_)


class TaskOrchestrator:
    def __init__(self):
        self.schedulers = {
            "background": create_scheduler("background"),
        }

    async def start(self):
        self.schedulers["background"].start_in_background()

    async def shutdown(self):
        self.schedulers["background"].remove_schedule("")

    async def add_task(self, task_config: TaskConfig):
        scheduler = self.schedulers.get(task_config.schedule_type, None)

        if scheduler:
            task = ScheduledTask(task_config)
            task.schedule(scheduler)

        else:
            invalid_message = f"Invalid scheduler type: {task_config.schedule_type}."
            available_message = f"Available schedulers: {self.schedulers.keys()}"
            raise ValueError(f"{invalid_message} {available_message}")

    def remove_task(self, schedule_type: str, task_name: str):
        scheduler = self._get_scheduler(schedule_type)
        try:
            scheduler.remove_schedule(task_name)
        except ScheduleLookupError:
            raise ValueError(
                f"Task '{task_name}' not found in scheduler '{schedule_type}'."
            )

    def list_tasks(self, schedule_type: str):
        scheduler = self._get_scheduler(schedule_type)
        return scheduler.get_jobs()

    def _get_scheduler(self, schedule_type: str):
        scheduler = self.schedulers.get(schedule_type)
        if not scheduler:
            invalid_message = f"Invalid scheduler type: {schedule_type}."
            available_message = f"Available schedulers: {list(self.schedulers.keys())}"
            raise ValueError(f"{invalid_message} {available_message}")

        return scheduler

    def remote_all_schedules_from(self, schedule_type: str):
        scheduler = self.schedulers.get(schedule_type)

        if scheduler:
            scheduler.remove_schedule()

    async def remote_all_schedules(self):
        self.schedulers["background"].remove_schedule("")


class TaskRegister:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def register(self, task_configs: List[TaskConfig]):
        for config in task_configs:
            # Prepare task data using TaskCreate Pydantic model
            task_data = TaskCreate(
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
                # Register the task using the repository's create method
                self.task_repository.create(task_data.model_dump())
            except Exception as e:
                logger.error(
                    f"Error trying to register TaskConfig {task_data.task_name}: {e}"
                )
