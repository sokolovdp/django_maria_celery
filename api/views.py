from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import ScheduledReward
from api.serializers import ScheduledRewardSerializer, UserSerializer


class ProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RewardsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ScheduledReward.objects.all()
    serializer_class = ScheduledRewardSerializer

    def get_queryset(self):
        return ScheduledReward.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="request")
    def award_request(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        award = serializer.create_award(serializer.validated_data)
        serializer = self.get_serializer(award)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
