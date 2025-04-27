import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_case.settings")

app = Celery("api_case")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    "process-rewards-hourly": {
        "task": "api.tasks.process_rewards",
        "schedule": crontab(minute="*/5"),  # Run every 5 minutes
    },
}
