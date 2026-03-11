#!/bin/bash
# Production run script using Gunicorn
# Usage: ./run_production.sh

# Set environment
export FLASK_ENV=production

# Run with Gunicorn
# - workers: 2-4 x CPU cores (default: 2)
# - bind: 0.0.0.0:5000
# - timeout: 120s for slow clients
# - keep-alive: 5s
# - access log: log/access.log
# - error log: log/error.log

gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile log/access.log \
    --error-logfile log/error.log \
    --log-level info \
    --capture-output \
    "app:app"
