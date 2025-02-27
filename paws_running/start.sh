#!/bin/bash

echo "🚀 Starting Celery Worker..."
celery -A paws_running.tasks.celery worker --loglevel=info &

echo "🚀 Starting Flask Server..."
gunicorn -w 4 -b 0.0.0.0:8000 paws_running.app:app
