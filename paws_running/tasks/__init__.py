import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "rediss://your-redis-host:6379")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.update(
    result_expires=3600  # Results expire in 1 hour
)
