from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from api.v1.actions.services import ActionService
from actions.choices import ActionEvent
from .services import UserProfileService
from .serializers import (ProfileSerializer,
                          UpdateProfileSerializer,
                          UpdateImageSerializer,
                          ChangePasswordSerializer)

User = get_user_model()


class ProfileAPIView(GenericAPIView):
    '''Собственный профайл пользователя.'''
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileSerializer
        elif self.request.method == 'POST':
            return UpdateProfileSerializer

    def get(self, request):
        user = UserProfileService().get_current_user(request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = UserProfileService.change_password(serializer.data, request.user)
        return Response({'status': data['status']}, status=data['status_code'])


class UpdateImageAPIView(GenericAPIView):
    serializer_class = UpdateImageSerializer

    def post(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ActionService(
            event=ActionEvent.UPDATE_AVATAR,
            user=request.user,
            content_object=request.user
        ).create_action()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfile(GenericAPIView):
    '''Профайл пользователя.'''
    lookup_field = 'id'
    serializer_class = ProfileSerializer

    def get(self, request, id):
        user = UserProfileService().get_user(self.request.user, id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
