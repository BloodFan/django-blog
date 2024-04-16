from dj_rest_auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .services import (AuthAppService, PasswordResetService,
                       PasswordResetToken, PasswordResetTokenConfirm,
                       full_logout)
from .addictional_service import LoginService

User = get_user_model()


class ConfirmView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.PasswordConfirmSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        user = service.validate_key(serializer.validated_data)
        service.activate_user(user)

        return Response(
            {'detail': 'Registration successfully completed'},
            status=status.HTTP_201_CREATED,
        )


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = AuthAppService()
        user = service.create_user(serializer.validated_data)
        service.send_message(user)
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


# class LoginView(GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = serializers.LoginSerializer

#     def post(self, request):
#         service = LoginService()

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         data = service.get_tokens(serializer.validated_data['user'])

#         jwt_serializer = serializers.JWTSerializer(data=data)
#         jwt_serializer.is_valid(raise_exception=True)

#         response = Response(jwt_serializer.data, status=status.HTTP_200_OK)
#         service.set_cookie(response)

#         return response


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PasswordResetService()
        service.password_handler(serializer.data['email'])

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetValidateView(GenericAPIView):
    serializer_class = serializers.PasswordResetValidateSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PasswordResetService()
        data = PasswordResetToken(**serializer.validated_data)
        service.decode_token_and_uid(data)
        return Response(
            {'detail': _('Token and uid validated successfully.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PasswordResetService()
        data = PasswordResetTokenConfirm(**serializer.validated_data)
        user = service.decode_token_and_uid(data)
        service.set_password(user, data.password_1)
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )
