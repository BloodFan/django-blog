import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.test.client import Client

from blog.models import Category, Tag, Article

pyteststmark = [pytest.mark.django_db]


User = get_user_model()


@pytest.fixture
def user() -> User:
    """User, подтвердивший активацию по email."""
    return User.objects.create_user(
        email='test_email@mail.com',
        password='test_password3210',
        first_name='test_first_name',
        last_name='test_last_name',
        is_active=True,
    )


@pytest.fixture
def auth_client(user):
    refresh = RefreshToken.for_user(user)
    headers = {'Authorization': f'Bearer {str(refresh.access_token)}'}
    return Client(headers=headers)


# @pytest.fixture
# def superuser() -> User:
#     """Superuser."""
#     return User.objects.create_superuser(
#         email='Zeus@mail.com',
#         password='XXXOverlordXXX111',
#         first_name='Перун',
#         last_name='Кроносов',
#         is_active=True,
#     )


@pytest.fixture
def category() -> Category:
    """Создание категории для тестирования."""
    return Category.objects.create(
        name='category_for_testing',
        slug='test_category'
    )


@pytest.fixture
def tags() -> Tag:
    """Создание тегов для тестирования."""
    tags_list = [
       Tag(name='Tag_for_testing_1', slug='test_Tag_1'),
       Tag(name='Tag_for_testing_2', slug='test_Tag_2'),
    ]
    return Tag.objects.bulk_create(tags_list)


@pytest.fixture
def article(category, tags, user) -> Article:
    """Создание Article для тестирования."""
    article = Article.objects.create(
        author=user,
        title='test_title',
        content='Абсолютно все, что угодно!',
        image='no-image-available.jpg',  #  путь к файлу а не base64
        category=category,
    )
    article.tags.set(tags)
    return article
