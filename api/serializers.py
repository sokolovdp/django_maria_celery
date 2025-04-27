from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from api.models import ScheduledReward, User

MAX_AMOUNT = 100


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "coins"]
        read_only_fields = ["coins"]


class ScheduledRewardSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_amount(value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        if value > MAX_AMOUNT:
            raise serializers.ValidationError(
                f"Amount must be less or equal to {MAX_AMOUNT}"
            )
        return value

    def validate(self, attrs: dict) -> dict:
        # Check if user already requested award today
        start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        if ScheduledReward.objects.filter(
            user=self.context["user"],
            created_at__range=[start, end],
        ).exists():
            raise serializers.ValidationError("Award can be requested once per day.")

        return attrs

    def create_award(self, validated_data: dict) -> ScheduledReward:
        # Create new award scheduled in 5 minutes
        return ScheduledReward.objects.create(
            user=self.context["user"],
            amount=validated_data["amount"],
            execute_at=timezone.now() + timedelta(minutes=5),
        )

    class Meta:
        model = ScheduledReward
        fields = ["amount", "execute_at", "is_executed", "created_at"]
        read_only_fields = ["execute_at", "is_executed", "created_at"]
