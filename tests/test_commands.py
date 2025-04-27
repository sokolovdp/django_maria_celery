from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from api.models import RewardLog, ScheduledReward

User = get_user_model()


class ProcessRewardsCommandTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="test_password",
        )
        # Create a reward that should be processed (past execution time)
        self.due_reward = ScheduledReward.objects.create(
            user=self.user, amount=100, execute_at=timezone.now() - timedelta(minutes=5)
        )
        # Create a reward that should not be processed yet (future execution time)
        self.future_reward = ScheduledReward.objects.create(
            user=self.user, amount=200, execute_at=timezone.now() + timedelta(minutes=5)
        )
        # Create a reward that's already been executed
        self.executed_reward = ScheduledReward.objects.create(
            user=self.user,
            amount=300,
            execute_at=timezone.now() - timedelta(minutes=10),
            is_executed=True,
        )

    def test_process_rewards(self):
        """Test the process_rewards command processes only due rewards"""
        # Capture command output
        out = StringIO()
        call_command("process_rewards", stdout=out)
        command_output = out.getvalue()

        # Verify command output
        self.assertIn("Successfully processed 1 rewards", command_output)
        self.assertIn(f"Processed reward: {self.due_reward}", command_output)

        # Refresh objects from database
        self.due_reward.refresh_from_db()
        self.future_reward.refresh_from_db()
        self.executed_reward.refresh_from_db()
        self.user.refresh_from_db()

        # Check that only due reward was processed
        self.assertTrue(self.due_reward.is_executed)
        self.assertFalse(self.future_reward.is_executed)
        self.assertTrue(self.executed_reward.is_executed)

        # Check user's coins were updated correctly
        self.assertEqual(self.user.coins, 100)  # Only the due reward amount

        # Check reward log was created
        reward_log = RewardLog.objects.filter(user=self.user).first()
        self.assertIsNotNone(reward_log)
        self.assertEqual(reward_log.amount, 100)
        self.assertEqual(
            reward_log.reason, f"Scheduled reward (ID: {self.due_reward.id})"
        )

    def test_process_rewards_no_pending(self):
        """Test the process_rewards command when there are no pending rewards"""
        # Execute the due reward first
        self.due_reward.execute()

        # Run command and capture output
        out = StringIO()
        call_command("process_rewards", stdout=out)
        command_output = out.getvalue()

        # Verify command output shows no rewards were processed
        self.assertIn("Successfully processed 0 rewards", command_output)

        # Verify no additional reward logs were created
        self.assertEqual(RewardLog.objects.count(), 1)
