from typing import TYPE_CHECKING
from django.db.models import Count, OuterRef, Subquery, Q, QuerySet, Exists
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.exceptions import NotFound

from blog.choices import ArticleStatus
from actions.models import Following

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class UserProfileService:
    def get_user(self, current_user: User, id: int) -> User:
        queryset = self.annotate_queryset_is_follower(current_user)
        try:
            return queryset.get(id=id)
        except User.DoesNotExist:
            raise NotFound({'Status': 'User not found.'})

    def get_current_user(self, current_user: User):
        ''' Прокладка. Причина - необходимость request.user для is_follower.'''
        return self.get_user(current_user, current_user.id)

    def user_queryset(self) -> QuerySet[User]:
        return User.objects.all().annotate(
            article_count=self.get_count('article_set'),
            comment_count=self.get_count('comment_set'),
            like_count=self.get_count('likes'),
        )

    def annotate_queryset_is_follower(self, current_user: User) -> QuerySet[User]:
        return self.user_queryset().annotate(
            is_follower=Exists(Following.objects.filter(user=current_user, author=OuterRef('id')))
        )

    def get_count(self, related_name: str) -> Coalesce:
        '''Получение count's. Причина метода - баг с перемножением.'''
        match related_name:
            case 'article_set':
                return Coalesce(
                    Subquery(
                        User.objects.filter(id=OuterRef('id'))
                        .annotate(count=Count(
                            related_name,
                            filter=Q(article_set__status=ArticleStatus.ACTIVE)
                        )).values('count')[:1]), 0)
            case _:
                return Coalesce(
                    Subquery(
                        User.objects.filter(id=OuterRef('id'))
                        .annotate(count=Count(related_name))
                        .values('count')[:1]), 0)

    @staticmethod
    def change_password(data: dict, user: User) -> dict:
        if user.check_password(data.get('old_password')):
            user.set_password(data.get('new_password1'))
            user.save()
            return {'status': 'Password changed successfully.', 'status_code': status.HTTP_200_OK}
        return {'status': 'Error - Incorrect old password.', 'status_code': status.HTTP_400_BAD_REQUEST}
