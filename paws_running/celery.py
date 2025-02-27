import os
from celery import Celery

# Redis URL ko environment variable se lein aur default value set karein
REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable not set!")

# Agar Redis SSL cert error ho to use fix karein
if REDIS_URL.startswith("rediss://") and "ssl_cert_reqs" not in REDIS_URL:
    REDIS_URL += "?ssl_cert_reqs=CERT_NONE"

def make_celery():
    celery = Celery(
        "paws_running",
        broker=REDIS_URL,
        backend=REDIS_URL
    )
    
    # Celery configurations
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True
    )
    
    return celery

celery = make_celery()
