import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "rediss://your-redis-host:6379")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# ✅ Add SSL Fix
celery.conf.update(
    broker_use_ssl={"ssl_cert_reqs": "CERT_NONE"},
    result_backend_use_ssl={"ssl_cert_reqs": "CERT_NONE"},
    result_expires=3600
)
