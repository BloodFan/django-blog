from urllib.parse import urljoin

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.reverse import reverse_lazy

User = get_user_model()


class ChatUserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'image',
            'url',
        )

    def get_url(self, obj: User) -> str:
        request = self.context['request']
        return request.build_absolute_uri(reverse_lazy('user_profile:profile', kwargs={'id': obj.id}))

    def get_image(self, obj: User) -> str:
        path = obj.image.url
        url = settings.FRONTEND_URL
        full_url = urljoin(url, path)
        return full_url


class ValidateJWTSerializer(serializers.Serializer):
    jwt = serializers.CharField(source='jwt_auth')


class IdSerializer(serializers.Serializer):
    id = serializers.CharField()
