from rest_framework import serializers

from actions.models import Like
from .services import LikeObjectsChoices
from main.models import User


class LikeSerializer(serializers.ModelSerializer):
    vote = serializers.ChoiceField(choices=Like.Vote.choices)
    model = serializers.ChoiceField(choices=LikeObjectsChoices.choices)

    class Meta:
        model = Like
        fields = (
            'vote',
            'object_id',
            'model'
        )


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
