from typing import Union

from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, OuterRef, Q, QuerySet, TextChoices
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from actions.choices import ActionEvent, ActionMeta, FollowingStatus, LikeStatus
from actions.models import Action, ActionUsers, Following, Like
from blog.models import Article, Comment

from ..user_profile.services import UserProfileService
from main.models import User, UserType


class LikeObjectsChoices(TextChoices):
    ARTICLE = ('article', 'Article')
    COMMENT = ('comment', 'Comment')


class LikeService:
    def __init__(self, object_id: int, vote: Like.Vote, user: UserType, model: LikeObjectsChoices) -> None:
        self.object_id = object_id
        self.vote = vote
        self.user = user
        self.model = model
        self.instance = self.get_model_instance()

    def get_article(self) -> Article:
        try:
            return Article.objects.get(id=self.object_id)
        except Article.DoesNotExist:
            raise NotFound('Article does not exist')

    def get_comment(self) -> Comment:
        try:
            return Comment.objects.get(id=self.object_id)
        except Comment.DoesNotExist:
            raise NotFound('Comment does not exist')

    def get_model_instance(self) -> Union[Article, Comment]:
        match self.model:
            case LikeObjectsChoices.ARTICLE:
                return self.get_article()
            case LikeObjectsChoices.COMMENT:
                return self.get_comment()

    def handler_like(self) -> dict:
        match self.instance.likes.filter(user=self.user).first():
            case Like() as like if (like.vote == self.vote):
                self.delete_like(like)
                return {
                    'status': LikeStatus.DOES_NOT_EXIST,
                    'model': self.model,
                    'object_id': self.object_id,
                    'status_code': status.HTTP_200_OK,
                }
            case Like() as like if (like.vote != self.vote):
                like = self.update_like(like)
                return {
                    'status': like.vote,
                    'model': self.model,
                    'object_id': self.object_id,
                    'status_code': status.HTTP_200_OK,
                }
            case _:
                like = self.create_like()
                return {
                    'status': like.vote,
                    'model': self.model,
                    'object_id': self.object_id,
                    'status_code': status.HTTP_201_CREATED,
                }

    def delete_like(self, like: Like) -> None:
        event = ActionService.get_event_type(self.instance)
        ActionService(
            event=event, user=self.user, content_object=self.instance
        ).delete_action()  # лента новостей(удаление)
        like.delete()

    def update_like(self, like: Like) -> Like:
        like.vote = self.vote
        like.save(update_fields=['vote'])
        return like

    def create_like(self) -> Like:
        event = ActionService.get_event_type(self.instance)
        ActionService(
            event=event,
            user=self.user,
            content_object=self.instance,
            meta=ActionMeta[event](),
        ).create_action()  # лента новостей
        return Like.objects.create(user=self.user, vote=self.vote, content_object=self.instance)


class FollowingService:
    def __init__(self, user, user_id):
        self.user = user
        self.user_id = user_id

    def subscribe_handler(self) -> FollowingStatus:
        if self.is_following():
            self.delete_following()
            return FollowingStatus.DOES_NOT_EXIST
        else:
            self.create_following()
            return FollowingStatus.EXISTS

    def create_following(self) -> Following:
        self.validate_subscription()
        return Following.objects.create(user=self.user, author_id=self.user_id)

    def delete_following(self):
        Following.objects.filter(user=self.user, author_id=self.user_id).delete()

    def is_following(
        self,
    ) -> bool:
        return Following.objects.filter(user=self.user, author_id=self.user_id).exists()

    def validate_subscription(self):
        if self.user.id == self.user_id:
            raise ValidationError('Нельзя подписаться на себя.')


class FollowingListService:
    def __init__(self, user: User):
        self.user = user

    def get_queryset(self) -> QuerySet[User]:
        queryset = UserProfileService().annotate_queryset_is_follower(self.user)
        return queryset


class ActionService:
    def __init__(
        self,
        event: ActionEvent,
        user: User,
        content_object: Union[Article, User, Comment],
        meta: Union[None, dict] = None,
    ) -> None:
        self.event = event
        self.user = user
        self.content_object = content_object
        self.meta = meta

    def is_action(self) -> bool:
        content_type = ContentType.objects.get_for_model(self.content_object)
        object_id = self.content_object.id
        return Action.objects.filter(
            event=self.event, user=self.user, content_type=content_type, object_id=object_id
        ).exists()

    def create_action(self) -> Action:
        return Action.objects.create(
            event=self.event, user=self.user, content_object=self.content_object, meta=self.meta or {}
        )

    def delete_action(self):
        if self.is_action():
            content_type = ContentType.objects.get_for_model(self.content_object)
            object_id = self.content_object.id
            Action.objects.get(
                event=self.event, user=self.user, content_type=content_type, object_id=object_id
            ).delete()

    @staticmethod
    def get_event_type(instance: Union[Article, Comment]) -> ActionEvent:
        match instance:
            case Comment():
                return ActionEvent.CREATE_LIKE_COMMENT
            case Article():
                return ActionEvent.CREATE_LIKE_ARTICLE


class ActionQueryset:
    def get_queryset(self, user: User) -> QuerySet[Action]:
        return (
            Action.objects.select_related('user')
            .prefetch_related('content_object')
            .annotate(
                is_follower=Exists(Following.objects.filter(user=user, author=OuterRef('user_id'))),
            )
            .filter(Q(is_follower=True) & ~Q(actionusers__user=user))
            .all()
        )

        # Альтернатива
        # return Action.objects.select_related('user').prefetch_related('content_object').annotate(
        #     is_follower=Exists(Following.objects.filter(user=user, author=OuterRef('user_id'))),
        #     is_familiarized=Exists(ActionUsers.objects.filter(user=user, action=OuterRef('id'))),
        # ).filter(Q(is_follower=True) & Q(is_familiarized=False)).all()


class ActionUsersService:
    def create_actionusers_relation(self, user: User, action_id: int) -> ActionUsers:
        '''Ознакомление пользователя с новостью.'''
        return ActionUsers.objects.create(user=user, action_id=action_id)
