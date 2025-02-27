import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "rediss://your-redis-host:6379")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# ✅ Secure Redis Connection Fix
celery.conf.update(
    broker_use_ssl={"ssl_cert_reqs": "CERT_NONE"},
    result_backend_use_ssl={"ssl_cert_reqs": "CERT_NONE"},
    result_expires=3600
)

# ✅ Fix ImportError (Check Functions)
from .tasks_list import add_task, complete_task, get_tasks

__all__ = ["add_task", "complete_task", "get_tasks", "celery"]
