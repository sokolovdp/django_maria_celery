#!/bin/bash

set -e

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate --no-input

echo "Starting Django server by Gunicorn..."
gunicorn api_case.wsgi:application \
    --timeout 60 \
    --workers 3 \
    --bind 0.0.0.0:8000
