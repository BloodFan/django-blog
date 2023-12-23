import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from blog.models import Article

pytestmark = [pytest.mark.django_db,]
User = get_user_model()
email_settings = override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CELERY_TASK_ALWAYS_EAGER=True
)


@email_settings
def test_create_article(auth_client, category, tags):
    """Интеграционный тест."""
    article_count = Article.objects.count()
    assert article_count == 0
    payload = {
        'title': 'test_title',
        'content': 'Абсолютно все, что угодно!',
        'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII=',
        'category': 1,
        'tags': [1, 2]
    }
    response = auth_client.post(
        path=reverse('api:v1:blog:articles-list'),
        data=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED

    article_count = Article.objects.count()
    article = Article.objects.first()

    assert article_count == 1

    payload = {
        'content': 'Ваш тестовый пост - это сущая лажа!',
    }

    response = auth_client.post(
        path=reverse('api:v1:blog:comments', kwargs={'slug': article.slug}),
        data=payload,
    )

    assert article.comment_set.count() == 1

    payload = {
        'content': 'И я горжусь этим!',
        'parent': article.comment_set.first().id
    }

    response = auth_client.post(
        path=reverse('api:v1:blog:comments', kwargs={'slug': article.slug}),
        data=payload,
    )

    assert article.comment_set.count() == 2
