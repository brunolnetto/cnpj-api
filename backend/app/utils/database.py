from datetime import datetime

from backend.app.api.dependencies.logs import get_app_start_logs_repository


def log_app_start():
    app_start_logs_repository = get_app_start_logs_repository()
    app_start_log = {"stlo_start_time": datetime.now()}
    app_start_logs_repository.create(app_start_log)
