from rest_framework import serializers
from django.contrib.auth import get_user_model
from base64 import b64decode
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from actions.models import Following

User = get_user_model()

error_messages = {
    'password_not_match': _('The two password fields did not match'),

}


class ProfileSerializer(serializers.ModelSerializer):
    # gender = serializers.CharField(source='get_gender_display')article_set comment_set
    article_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    like_count = serializers.IntegerField()
    is_follower = serializers.BooleanField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'birthday',
            'gender',
            'email',
            'article_count',
            'comment_count',
            'like_count',
            'image',
            'is_follower',
        )


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'birthday',
            'gender',
            'email',
        )


class UpdateImageSerializer(UpdateProfileSerializer):
    image = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ('image',)

    def validate_image(self, image: str):
        mime_type, raw_image = image.split(';base64,')
        image = b64decode(raw_image)
        extention = mime_type.split('/')[-1]
        return ContentFile(image, f'name_image.{extention}')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_new_password1(self, password: str):
        user = self.context['request'].user
        validate_password(password, user)
        return password

    def validate(self, data: dict):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'password_2': error_messages['password_not_match']})
        return data
