from rest_framework import serializers

from actions.models import Action, ActionUsers, Like
from blog.models import Article, Comment

from .services import LikeObjectsChoices
from main.models import User


class LikeSerializer(serializers.ModelSerializer):
    vote = serializers.ChoiceField(choices=Like.Vote.choices)
    model = serializers.ChoiceField(choices=LikeObjectsChoices.choices)

    class Meta:
        model = Like
        fields = ('vote', 'object_id', 'model')


class FollowingCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class FollowingSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    is_follower = serializers.BooleanField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'url',
            'full_name',
            'image',
            'is_follower',
        )


class UserSerializer(serializers.ModelSerializer):
    """Предназначен для ActionSerializer"""

    url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'url',
            'image',
        )


class ArticleSerializer(serializers.ModelSerializer):
    """Предназначен для ActionSerializer"""

    url = serializers.CharField(source='get_absolute_url')
    type = serializers.CharField(default='article', read_only=True)

    class Meta:
        model = Article
        fields = ('title', 'url', 'type')


class CommentSerializer(serializers.ModelSerializer):
    """Предназначен для ActionSerializer"""

    title = serializers.CharField(source='article.title')
    url = serializers.CharField(source='article.get_absolute_url')
    type = serializers.CharField(default='comment', read_only=True)

    class Meta:
        model = Comment
        fields = ('title', 'url', 'type')


class ActionSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Action
        fields = '__all__'

    def get_content_object(self, obj: Action) -> dict:
        match obj.content_object:
            case User() as user:
                data = UserSerializer(user).data
                return data
            case Article() as article:
                data = ArticleSerializer(article).data
                return data
            case Comment() as comment:
                data = CommentSerializer(comment).data
                return data
            case _:
                pass


class ActionUsersCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ActionUsers
        fields = ('id',)
