from typing import TYPE_CHECKING

from rest_framework.exceptions import NotFound
from rest_framework.filters import BaseFilterBackend

from main.models import User

if TYPE_CHECKING:  # убирает ошибку цикличного импорта
    from api.v1.actions.views import FollowingListAPIView


class SubscriptionFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view: "FollowingListAPIView"):
        user = request.user
        if id := request.query_params.get('user_id'):
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise NotFound('User does not exists.')

        search = request.query_params.get('search')
        if search == 'following':
            return queryset.filter(following=user)
        elif search == 'followers':
            return queryset.filter(followers=user)
