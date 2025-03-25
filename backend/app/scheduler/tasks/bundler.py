from backend.app.scheduler.tasks.logs import cleanup_debug_config
from backend.app.scheduler.tasks.logs import cleanup_request_config
from backend.app.scheduler.tasks.logs import cleanup_task_config

task_configs = [
    cleanup_request_config,
    cleanup_task_config,
    cleanup_debug_config,
]
