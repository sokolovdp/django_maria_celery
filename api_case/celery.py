import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_case.settings")

app = Celery("api_case")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
