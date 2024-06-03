from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class LoginService:
    def get_tokens(self, user: User) -> dict:
        self.access_token = str(AccessToken.for_user(user))
        self.refresh_token = str(RefreshToken.for_user(user))

        self.access_token_expiration = (timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        self.refresh_token_expiration = (timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

        data = {'access': self.access_token, 'refresh': self.refresh_token}
        return data

    def set_cookie(self, response: Response) -> Response:
        access_token_key = settings.REST_AUTH['JWT_AUTH_COOKIE']
        refresh_token_key = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']
        response.set_cookie(
            key=access_token_key,
            value=self.access_token,
            expires=self.access_token_expiration,
        )
        response.set_cookie(
            key=refresh_token_key,
            value=self.refresh_token,
            expires=self.refresh_token_expiration,
        )
        return response
