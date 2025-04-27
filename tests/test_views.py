from datetime import timedelta

from parameterized import parameterized

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from api.models import ScheduledReward

User = get_user_model()


class ViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="test_user",
            password="test_password",
        )
        self.client.force_authenticate(user=self.user)

    def test_scheduled_reward_list(self):
        """Test that users can only see their own scheduled rewards"""

        ScheduledReward.objects.create(
            user=self.user, amount=100, execute_at=timezone.now() + timedelta(days=1)
        )
        response = self.client.get("/api/rewards/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["amount"], 100)

    @parameterized.expand(
        [
            ("post", "post", None),
            ("put", "put", None),
            ("delete", "delete", None),
            ("patch", "patch", None),
        ]
    )
    def test_scheduled_reward_methods_not_allowed(self, name, method_name, expected):
        """Test that only GET method is allowed for rewards"""
        data = {
            "user": self.user.id,
            "amount": 150,
            "execute_at": (timezone.now() + timedelta(days=2)).isoformat(),
        }
        method = getattr(self.client, method_name)
        response = method("/api/rewards/", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_view(self):
        """Test that users can view their profile"""
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["username"], "test_user")

    @parameterized.expand(
        [
            ("post", "post", None),
            ("put", "put", None),
            ("delete", "delete", None),
            ("patch", "patch", None),
        ]
    )
    def test_profile_methods_not_allowed(self, name, method_name, expected):
        """Test that only GET method is allowed for profile"""
        method = getattr(self.client, method_name)
        response = method("/api/profile/", {"username": "new_name"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @parameterized.expand(
        [
            ("profile", "/api/profile/", None),
            ("rewards", "/api/rewards/", None),
            ("request", "/api/rewards/request/", None),
        ]
    )
    def test_unauthorized_access(self, name, endpoint, expected):
        """Test that unauthorized users cannot access the endpoints"""
        self.client.force_authenticate(user=None)
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_award_request_success(self):
        """Test successful award request"""
        response = self.client.post("/api/rewards/request/", {"amount": 100})
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

        award = ScheduledReward.objects.latest("created_at")
        self.assertEqual(award.user, self.user)
        self.assertEqual(award.amount, 100)
        self.assertFalse(award.is_executed)

        # Check execution time is about 5 minutes in the future
        time_diff = award.execute_at - timezone.now()
        self.assertGreater(time_diff.total_seconds(), 290)  # At least 4:50 minutes
        self.assertLess(time_diff.total_seconds(), 310)  # At most 5:10 minutes

    def test_award_request_once_per_day(self):
        """Test that user can only request award once per day"""
        # First request should succeed
        response = self.client.post("/api/rewards/request/", {"amount": 100})
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

        # Second request should fail
        response = self.client.post("/api/rewards/request/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Award can be requested once per day", str(response.content))

    @parameterized.expand(
        [
            ("minus", -11, None),
            ("zero", 0, None),
            ("too_big", 100000, None),
        ]
    )
    def test_award_request_with_invalid_amount(self, name, amount, expected):
        """Test that award request with invalid amount fails"""

        response = self.client.post("/api/rewards/request/", {"amount": amount})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Amount must be", str(response.content))
