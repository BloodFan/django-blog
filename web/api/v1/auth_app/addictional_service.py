from typing import TYPE_CHECKING, NamedTuple, Optional

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class LoginService:

    def get_tokens(self, user: User) -> dict:
        self.access_token = str(AccessToken.for_user(user))
        self.refresh_token = str(RefreshToken.for_user(user))

        # access_token_expiration = (timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        # refresh_token_expiration = (timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

        data = {
            'access': self.access_token,
            'refresh': self.refresh_token
        }
        return data

    def set_cookie(self, response: Response) -> Response:
        access_token_key = settings.REST_AUTH['JWT_AUTH_COOKIE']
        refresh_token_key = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']
        response.set_cookie(access_token_key, self.access_token)
        response.set_cookie(refresh_token_key, self.refresh_token)
        return response
