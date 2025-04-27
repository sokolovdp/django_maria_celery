FROM python:3.13-bookworm

# Set environment variables in a single layer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install system dependencies and clean up in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory to avoid relative paths
WORKDIR /app

# Copy only requirements files first for caching
COPY requirements.txt requirements_prod.txt ./

# Upgrade pip and install dependencies in one layer
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_prod.txt

# Copy application code and entrypoints
COPY api_case/ ./api_case/
COPY api/ ./api/
COPY static/ ./static/
COPY staticfiles/ ./staticfiles/
COPY manage.py start-api.sh start-celery-worker.sh start-celery-beat.sh ./

# Ensure entrypoints are executable
RUN chmod +x ./start-*.sh

# Use non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
