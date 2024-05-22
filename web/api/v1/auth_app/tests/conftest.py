import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


@pytest.fixture
def user_inactive() -> User:
    """User, не подтвердивший активацию по email."""
    return User.objects.create_user(
        email='test_email@mail.com',
        password='test_password3210',
        first_name='test_first_name',
        last_name='test_last_name',
        is_active=False,
    )


@pytest.fixture
def payload_uid_and_token(user) -> dict:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    payload = {'token': token, 'uid': uid}
    return payload
