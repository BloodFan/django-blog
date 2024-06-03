'''
GET /api/v1/chat/users?user_id=2&user_id=3
GET /api/v1/chat/users?user_ids=2,3,4
POST /api/v1/chat/users; {'users': [2,3,4]}
 '''

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .permissions import IsKeyInHeaders
from .serializers import ChatUserSerializer, IdSerializer, ValidateJWTSerializer
from .services import ChatUserService

User = get_user_model()


class ChatUserAPIView(GenericAPIView):
    serializer_class = ChatUserSerializer
    permission_classes = []

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_ids = self.request.query_params.get('user_ids')
        if user_ids is None:
            raise NotFound({'Status': 'Users not found.'})
        return ChatUserService().get_queryset(user_ids)


class ValidateInitChatUserAPIView(GenericAPIView):
    serializer_class = ChatUserSerializer
    permission_classes = []

    def post(self, request):
        service = ChatUserService()
        users_list = service.users_handler(request.data)
        serializer = self.get_serializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataByJWTAPIView(GenericAPIView):
    serializer_class = ValidateJWTSerializer
    permission_classes = [IsKeyInHeaders]

    def post(self, request):
        jwt_serializer = self.get_serializer(request.data)  # data from get_serializer(key) pass to swagger
        service = ChatUserService()
        user = service.decode_jwt(jwt_serializer.data['jwt'])
        serializer = ChatUserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataByIdAPIView(GenericAPIView):
    serializer_class = IdSerializer
    # permission_classes = [IsKeyInHeaders]

    def post(self, request):
        id_serializer = self.get_serializer(request.data)  # data from get_serializer(key) pass to swagger
        service = ChatUserService()
        user = service.get_user(id_serializer.data['id'])
        serializer = ChatUserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
