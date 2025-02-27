#!/bin/bash
echo "🚀 Starting Flask Server..."

# Redis + Celery Ensure Active
redis-server --daemonize yes
celery -A paws_running.tasks worker --loglevel=info &

# Gunicorn with Eventlet
exec gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 paws_running.app:app
