from app.config import settings

broker_url = settings.REDIS_URL
result_backend = settings.RESULT_BACKEND
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
task_track_started = True
worker_hijack_root_logger = False
