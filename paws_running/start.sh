#!/bin/bash
echo "🚀 Starting Flask Server..."
gunicorn -k eventlet -w 1 -b 0.0.0.0:10000 paws_running.app:app
