import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]
User = get_user_model()
email_settings = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', CELERY_TASK_ALWAYS_EAGER=True
)


class TestValidateKey:
    @pytest.fixture
    def confirmation_key(self, user_inactive) -> str:
        return user_inactive.confirmation_key

    def test_falsification_key(self, client, confirmation_key):
        """Тест модифицированного ключа."""
        confirmation_key += 'falsification'
        confirm = {'key': confirmation_key}
        response = client.post(
            path=reverse('api:v1:auth_app:confirm'),
            data=confirm,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_remote_user_key(self, client, user_inactive, confirmation_key):
        """Тест ключа удаленного user'a."""
        user_inactive.delete()
        confirm = {'key': confirmation_key}
        response = client.post(
            path=reverse('api:v1:auth_app:confirm'),
            data=confirm,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_expired_key(self, client, freezer, confirmation_key):
        """Тест просроченного ключа."""
        confirm = {'key': confirmation_key}
        freezer.tick(delta=3 * 24 * 3600)
        response = client.post(
            path=reverse('api:v1:auth_app:confirm'),
            data=confirm,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_success_key(self, client, confirmation_key):
        """Успешный тест ключа."""
        confirm = {'key': confirmation_key}
        response = client.post(
            path=reverse('api:v1:auth_app:confirm'),
            data=confirm,
        )
        assert response.status_code == status.HTTP_201_CREATED
