#!/bin/bash

echo "🚀 Starting Redis Server..."
redis-server &

echo "🚀 Starting Celery Worker..."
celery -A tasks.celery worker --loglevel=info &

echo "🚀 Starting Flask Server..."
gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 paws_running.app:app

