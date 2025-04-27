from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, RewardsViewSet

router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")
router.register("rewards", RewardsViewSet, basename="rewards")


urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
