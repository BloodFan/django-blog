from typing import TypedDict
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from main.models import UserType

User: UserType = get_user_model()


class RequestDataT(TypedDict):
    jwt_auth: str
    user_id: str


class ChatUserService:

    def get_queryset(self, user_ids: str) -> QuerySet[User]:
        users_list = user_ids.split(',')
        return User.objects.filter(id__in=users_list).all()

    def decode_jwt(self, token: str) -> User:
        try:
            decoded_token = AccessToken(token)
            user = User.objects.get(id=decoded_token['user_id'])
        except TokenError:
            raise ValidationError('Invalid jwt.')
        except User.DoesNotExist:
            raise NotFound('User not found.')
        return user

    def get_user(self, user_id: int | str) -> User:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound('User not found.')

    def users_handler(self, data: RequestDataT) -> list[User]:
        request_user = self.decode_jwt(data['jwt_auth'])
        user = self.get_user(data['user_id'])
        return [request_user, user]
