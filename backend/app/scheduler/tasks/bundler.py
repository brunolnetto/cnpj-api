from backend.app.scheduler.tasks.logs import (
    cleanup_request_config,
    cleanup_task_config,
    cleanup_debug_config,
    lookup_and_update_ip_info_config,
)

task_configs = [
    cleanup_request_config,
    cleanup_task_config,
    cleanup_debug_config,
    lookup_and_update_ip_info_config,
]
