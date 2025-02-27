#!/bin/bash
echo "🚀 Starting Flask Server..."

# Redis Background Me Run Karo
redis-server --daemonize yes

# Celery Worker Background Me Chalao
celery -A paws_running.tasks worker --loglevel=info &

# Gunicorn Ko Correctly Start Karo
exec gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 paws_running.app:app
