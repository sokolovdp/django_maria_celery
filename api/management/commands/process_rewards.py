from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import ScheduledReward


class Command(BaseCommand):
    help = "Process all pending scheduled rewards"

    def handle(self, *args, **options):
        pending_rewards = ScheduledReward.objects.filter(
            is_executed=False, execute_at__lte=timezone.now()
        )

        count = 0
        for reward in pending_rewards:
            if reward.execute():
                count += 1
                self.stdout.write(f"Processed reward: {reward}")

        self.stdout.write(f"Successfully processed {count} rewards")
