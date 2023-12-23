from django.utils.translation import gettext_lazy as _
from django.db.models import IntegerChoices, TextChoices
from enum import Enum


class LikeStatus(IntegerChoices):
    LIKE = 1
    DISLIKE = 0
    DOES_NOT_EXIST = 2


class FollowingStatus(Enum):
    EXISTS = True
    DOES_NOT_EXIST = False


class ActionEvent(TextChoices):
    CREATE_ARTICLE = 'create_article'
    UPDATE_AVATAR = 'update_avatar'
