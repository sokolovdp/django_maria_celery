from celery import shared_task

from django.core.management import call_command


@shared_task
def process_rewards():
    """Process scheduled rewards that are due."""
    call_command("process_rewards")
