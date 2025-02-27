import os
from celery import Celery

# Redis URL ko environment variable se lo, aur SSL error fix karo
REDIS_URL = os.getenv("REDIS_URL", "rediss://<your_redis_url>?ssl_cert_reqs=CERT_NONE")

def make_celery():
    celery = Celery(
        "paws_running",
        broker=REDIS_URL,
        backend=REDIS_URL
    )
    
    # Agar extra configurations add karni ho to yaha karein
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json'
    )
    
    return celery

celery = make_celery()
