#!/bin/bash

set -e

echo "Starting Celery worker..."
celery -A api_case worker --loglevel=info
