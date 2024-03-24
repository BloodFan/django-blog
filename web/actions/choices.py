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
    CREATE_COMMENT = 'create_comment'
    CREATE_LIKE_ARTICLE = 'create_like_article'
    CREATE_LIKE_COMMENT = 'create_like_comment'
    UPDATE_AVATAR = 'update_avatar'


class MetaTemplate:
    '''Шаблоны для ActionMeta(JSONField)'''
    @staticmethod
    def update_avatar_template(image: str) -> dict:
        return {
            'type': 'update_avatar',
            'image': f'/media/{image}'
        }

    @staticmethod
    def create_comment_template():
        '''заготовка для возможного расширения.'''
        return {'type': 'create_comment'}

    @staticmethod
    def create_article_template():
        '''заготовка для возможного расширения.'''
        return {'type': 'create_article'}

    @staticmethod
    def create_like_article_template():
        '''заготовка для возможного расширения.'''
        return {'type': 'create_like_article'}

    @staticmethod
    def create_like_comment_template():
        '''заготовка для возможного расширения.'''
        return {'type': 'create_like_comment'}


ActionMeta = {
    ActionEvent.UPDATE_AVATAR: MetaTemplate.update_avatar_template,
    ActionEvent.CREATE_COMMENT: MetaTemplate.create_comment_template,
    ActionEvent.CREATE_ARTICLE: MetaTemplate.create_article_template,
    ActionEvent.CREATE_LIKE_ARTICLE: MetaTemplate.create_like_article_template,
    ActionEvent.CREATE_LIKE_COMMENT: MetaTemplate.create_like_comment_template,
}
