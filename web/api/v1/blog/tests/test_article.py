import re

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from blog.choices import ArticleStatus
from blog.models import Article

pytestmark = [
    pytest.mark.django_db,
]
User = get_user_model()
email_settings = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', CELERY_TASK_ALWAYS_EAGER=True
)


@email_settings
def test_create_article(auth_client, category, tags, admin_client):
    """Создание блога."""
    article_count = Article.objects.count()
    assert article_count == 0
    payload = {
        'title': 'test_title',
        'content': 'Абсолютно все, что угодно!',
        'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEUAAACnej3aAAAAAXR'
                 'STlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII=',
        'category': 1,
        'tags': [1, 2],
    }
    response = auth_client.post(
        path=reverse('api:v1:blog:articles-list'),
        data=payload,
    )

    article_count = Article.objects.count()
    article = Article.objects.order_by("-id")[0]  # first()

    assert response.status_code == status.HTTP_201_CREATED
    assert article_count == 1
    # пост создан

    assert article.status == ArticleStatus.INACTIVE
    # пост невиден пользователю

    assert len(mail.outbox) == 2
    # Создается 2 сообщения

    assert mail.outbox[0].to[0] == article.author.email
    # Уходит сообщение создателю поста

    assert mail.outbox[1].to[0] == settings.ADMIN_EMAIL
    # Уходит сообщение администратору

    string = mail.outbox[1].alternatives[0][0]
    id = int(re.findall(r'(?<=/admin/blog/article/).+(?=/change/)', string)[0])

    assert id == article.id
    # Админу отправляется ссылка с корректным id

    response = admin_client.post(
        # path=f'/admin/blog/article/{id}/change/',
        path=reverse(f'admin:{article._meta.app_label}_{type(article).__name__.lower()}_change', args=(id,)),
        data={'_make-active': 'Make Active'},  # status article не обновляется
    )
    # article._meta.app_label название приложение модели - blog
    # type(article).__name__.lower() название модели - article
    assert response.status_code == status.HTTP_200_OK

    article = Article.objects.first()
    # article.status = ArticleStatus.ACTIVE

    assert article.status == ArticleStatus.ACTIVE
