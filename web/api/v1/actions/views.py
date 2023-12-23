from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import (LikeSerializer, FollowingCreateSerializer,
                          FollowingSerializer)
from .services import (LikeService, FollowingService,
                       FollowingListService)
from actions.models import Like
from main.models import User
from ..user_profile.filters import SubscriptionFilter


class LikeApiView(GenericAPIView):
    serializer_class = LikeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = LikeService(**serializer.validated_data, user=request.user)
        data = service.handler_like()
        return Response(
            {
                'status': data['status'],
                'model': data['model'],
                'object_id': data['object_id']
            },
            status=data['status_code']
        )

    def get(self, request):
        queryset = Like.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FollowingApiView(GenericAPIView):

    serializer_class = FollowingCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = FollowingService(request.user, serializer.data['user_id'])
        status = service.subscribe_handler()
        return Response({'status': status.value})


class FollowingListAPIView(GenericAPIView):
    serializer_class = FollowingSerializer
    filter_backends = (SubscriptionFilter,)

    def get(self, request):
        service = FollowingListService(request.user)
        queryset = service.list_handler()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
