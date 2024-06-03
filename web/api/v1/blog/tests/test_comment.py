import pytest

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from blog.models import Article

pytestmark = [
    pytest.mark.django_db,
]
User = get_user_model()
email_settings = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', CELERY_TASK_ALWAYS_EAGER=True
)


def test_create_comment(auth_client, article):
    article = Article.objects.first()

    payload = {
        'content': 'Ваш тестовый пост - это сущая лажа!',
    }

    response = auth_client.post(
        path=reverse('api:v1:blog:comments', kwargs={'slug': article.slug}),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert article.comment_set.count() == 1

    payload = {'content': 'И я горжусь этим!', 'parent': article.comment_set.first().id}

    response = auth_client.post(
        path=reverse('api:v1:blog:comments', kwargs={'slug': article.slug}),
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert article.comment_set.count() == 2
