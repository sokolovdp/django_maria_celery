from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class ScheduledReward(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="scheduled_rewards",
        verbose_name="User",
    )
    amount = models.IntegerField(verbose_name="Amount of coins", default=0)
    execute_at = models.DateTimeField(verbose_name="Execution time")
    is_executed = models.BooleanField(default=False, verbose_name="Is executed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Scheduled awards"
        verbose_name_plural = "Scheduled awards"
        ordering = ["execute_at"]

    def __str__(self):
        return f"{self.amount} coins to be given for {self.user.username} at {self.execute_at}"

    def execute(self):
        if not self.is_executed and timezone.now() >= self.execute_at:
            self.user.coins += self.amount
            self.user.save()

            # Create reward log
            RewardLog.objects.create(
                user=self.user,
                amount=self.amount,
                reason=f"Scheduled reward (ID: {self.id})",
            )

            self.is_executed = True
            self.save()
            return True

        return False


class RewardLog(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="reward_logs",
        verbose_name="User",
    )
    amount = models.IntegerField(verbose_name="Coins amount")
    given_at = models.DateTimeField(auto_now_add=True, verbose_name="Time of reward")
    reason = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Award reason"
    )

    class Meta:
        verbose_name = "Reward log"
        verbose_name_plural = "Reward logs"
        ordering = ["-given_at"]

    def __str__(self):
        return (
            f"{self.amount} coins was given to {self.user.username} at {self.given_at}"
        )
