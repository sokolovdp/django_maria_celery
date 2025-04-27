from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils import timezone

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        post_migrate.connect(self.update_periodic_tasks, sender=self)

    def update_periodic_tasks(self, *args, **kwargs):
        from django_celery_beat.models import CrontabSchedule, PeriodicTask

        crontab_every_minute, _ = CrontabSchedule.objects.get_or_create(
            minute="*",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )
        task, created = PeriodicTask.objects.get_or_create(
            name="process_rewards",
            task="api.tasks.process_rewards",
            crontab=crontab_every_minute,
        )
        if created:
            task.start_time = timezone.now()
            task.save()
