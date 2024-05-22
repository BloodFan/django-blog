from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from actions.models import Like

from ..user_profile.filters import SubscriptionFilter
from .serializers import (
    ActionSerializer,
    ActionUsersCreateSerializer,
    FollowingCreateSerializer,
    FollowingSerializer,
    LikeSerializer,
)
from .services import ActionQueryset, ActionUsersService, FollowingListService, FollowingService, LikeService


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
                'object_id': data['object_id'],
            },
            status=data['status_code'],
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
        queryset = service.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActionListAPIView(GenericAPIView):
    serializer_class = ActionSerializer

    def get(self, request):
        queryset = ActionQueryset().get_queryset(request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActionUsersAPIView(GenericAPIView):
    serializer_class = ActionUsersCreateSerializer

    def post(self, request):
        '''Ознакомление пользователя с новостью.'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ActionUsersService()
        service.create_actionusers_relation(user=request.user, action_id=serializer.data['id'])
        return Response(status=status.HTTP_201_CREATED)
