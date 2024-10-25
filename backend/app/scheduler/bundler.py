import asyncio

from backend.app.scheduler.base import TaskOrchestrator, TaskRegister
from backend.app.api.repositories.tasks import get_task_repository
from backend.app.scheduler.tasks.bundler import task_configs
from backend.app.setup.logging import logger

task_orchestrator = TaskOrchestrator()


async def add_tasks():
    """
    Create a task orchestrator and add tasks to it.

    This function checks for existing tasks in the database to avoid duplication.
    It uses the task configurations defined in `task_configs`, which contains instances of TaskConfig.

    Raises:
        Exception: If there are issues during task registration.
    """
    task_repository = get_task_repository()
    # Ensure this is an async call if needed
    existing_tasks = task_repository.get_all()

    # Use a set for fast lookup
    existing_task_ids = {task.task_id for task in existing_tasks}

    task_register = TaskRegister(task_repository)

    for task_config in task_configs:
        if task_config.task_id in existing_task_ids:
            # Skip adding duplicate tasks
            continue

        # Add the task to the orchestrator
        await task_orchestrator.add_task(task_config)

        # Save the new task to the database using the repository
        try:
            # Register as a list if the method requires it
            task_register.register([task_config])
        except Exception as e:
            logger.error(
                f"Error registering task {task_config.task_name}: {e}")

    await asyncio.sleep(1)
