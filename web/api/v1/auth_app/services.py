from typing import TYPE_CHECKING, NamedTuple, Optional
from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.db import transaction
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_services import BaseEmailHandler
from auth_app.choices import error_messages

from main import tasks
from main.decorators import except_shell

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str
    gender: str
    birthday: str


class ConfirmEmail(NamedTuple):
    key: str


class PasswordResetToken(NamedTuple):
    token: str
    uid: str


class PasswordResetTokenConfirm(NamedTuple):
    token: str
    uid: str
    password_1: str
    password_2: str


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = '/confirm'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def get_user_from_uid(uid: str):
        uid = urlsafe_base64_decode(force_str(uid))
        return User.objects.get(id=uid)

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        user = User.objects.create_user(
            email=data.email,
            password=data.password_1,
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=False,
            gender=data.gender,
            birthday=data.birthday,
        )
        return user

    @staticmethod
    def validate_key(validated_data: dict) -> User:
        """Проверка ключа подтверждения отправляемого на email."""
        response = ConfirmEmail(**validated_data)
        key = response.key
        try:
            user_id = signing.loads(key, max_age=settings.EMAIL_CONFIRMATION_EXPIRE_DAYS)
            user = User.objects.get(id=user_id)
        except (signing.BadSignature, signing.SignatureExpired, User.DoesNotExist):
            raise ValidationError('Error: invalid confirmation key')
        return user

    @staticmethod
    def activate_user(user: User):
        user.is_active = True
        user.save(update_fields=['is_active'])

    @staticmethod
    def send_message(user: User):
        template_name = 'emails/confirmation.html'
        user_id = user.confirmation_key
        context = {'user_id': user_id, 'full_name': user.full_name, 'frontend_url': settings.FRONTEND_URL}
        subject = 'Добро пожаловать111!'

        print(f'{user.email=}')
        print(f'{user.email=}')

        tasks.send_information_email.delay(
            subject=subject,
            template_name=template_name,
            context=context,
            to_email=user.email,
            from_email=settings.ADMIN_EMAIL,
        )

    @staticmethod
    def validate_user(email: str, password: str, user: User):
        """Проверка существования и активности пользователя."""
        if not user:
            user = AuthAppService.get_user(email)
            if not user:
                msg = {'email': error_messages['wrong_credentials']}
                raise serializers.ValidationError(msg)
            if not user.is_active:
                msg = {'email': error_messages['not_active']}
                raise serializers.ValidationError(msg)
            msg = {'email': error_messages['wrong_credentials']}
            raise serializers.ValidationError(msg)


class PasswordResetService:
    def get_user(self, email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def create_key(self, user: User) -> PasswordResetToken:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        return PasswordResetToken(token=token, uid=uid)

    def password_handler(self, email: str):
        user = self.get_user(email)
        if not user:
            return
        tokens = self.create_key(user)
        self.send_message(user, tokens)

    def send_message(self, user: User, tokens: PasswordResetToken):
        template_name = 'emails/reset_password.html'
        context = {
            'full_name': user.full_name,
            'url': f'{settings.FRONTEND_URL}confirm_reset_password/' f'?token={tokens.token}&uid={tokens.uid}',
        }
        subject = 'Восстановление пароля, проект django-blog.'

        tasks.send_information_email.delay(
            subject=subject, template_name=template_name, context=context, to_email=user.email
        )

    def decode_token_and_uid(self, data: NamedTuple) -> User:
        try:
            uid = urlsafe_base64_decode(force_str(data.uid))
            user = User.objects.get(id=uid)
            token = default_token_generator.check_token(user, data.token)
            if not token:
                raise ValidationError('Invalid token.')
        except (User.DoesNotExist, ValueError):
            raise ValidationError('Invalid uid.')
        return user

    def set_password(self, user: User, password: str):
        user.set_password(password)
        user.save(update_fields=['password'])


def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    auth_cookie_name = settings.REST_AUTH['JWT_AUTH_COOKIE']
    refresh_cookie_name = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']

    response.delete_cookie(auth_cookie_name)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except KeyError:
        response.data = {"detail": _("Refresh token was not included in request data.")}
        response.status_code = status.HTTP_401_UNAUTHORIZED
    except (TokenError, AttributeError, TypeError) as error:
        if hasattr(error, 'args'):
            if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                response.data = {"detail": _(error.args[0])}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response.data = {"detail": _("An error has occurred.")}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response
