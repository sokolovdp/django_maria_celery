#!/bin/bash

set -e

echo "Starting Celery beat..."
celery -A api_case beat --loglevel=info
