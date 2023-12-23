import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db,]
User = get_user_model()
email_settings = override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CELERY_TASK_ALWAYS_EAGER=True
)


@email_settings
def test_email_does_not_exist(client):
    payload = {'email': 'invalid_email@gmail.com'}
    response = client.post(
        path=reverse('api:v1:auth_app:reset-password'),
        data=payload
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 0


class TestValidateUidAndToken:

    def test_falsification_uid(self, client, payload_uid_and_token):
        """Тест модифицированного uid."""
        payload_uid_and_token['uid'] += 'falsification'
        response = client.post(
            path=reverse('api:v1:auth_app:reset-password-validate'),
            data=payload_uid_and_token
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_remote_user_uid(self, client, user, payload_uid_and_token):
        """Тест uid удаленного user'a."""
        user.delete()
        response = client.post(
            path=reverse('api:v1:auth_app:reset-password-validate'),
            data=payload_uid_and_token
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_falsification_token(self, client, payload_uid_and_token):
        """Тест модифицированного token."""
        payload_uid_and_token['token'] += 'falsification'
        response = client.post(
            path=reverse('api:v1:auth_app:reset-password-validate'),
            data=payload_uid_and_token
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_success_validate(self, client, payload_uid_and_token):
        """Успешная проверка."""
        response = client.post(
            path=reverse('api:v1:auth_app:reset-password-validate'),
            data=payload_uid_and_token
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'password, expected_status', (
        ({'password_1': 'test_password3210', 'password_2': 'test_password3210'},
         status.HTTP_200_OK),
        ({'password_1': 'test_password3210', 'password_2': 'test_password'},
         status.HTTP_400_BAD_REQUEST),  # unmatched passwords
    )
)
def test_confirm_password(client, payload_uid_and_token, password, expected_status):
    """Проверка восстановления забытого пароля после валидации."""
    payload = payload_uid_and_token | password
    response = client.post(
        path=reverse('api:v1:auth_app:reset-password-confirm'),
        data=payload
    )
    print(f'{response.data=}')
    assert response.status_code == expected_status


# ИНТЕГРАЦИОННЫЙ ТЕСТ

@email_settings
def test_password_reset(client, user):
    payload = {'email': user.email}
    response = client.post(
        path=reverse('api:v1:auth_app:reset-password'),
        data=payload
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 1
    # отправка письма успешно

    string = mail.outbox[0].alternatives[0][0]
    token = re.findall(r'(?<=token=).+(?=&)', string)[0]
    uid = re.findall(r'(?<=uid=).+(?=")', string)[0]
    payload = {'token': token, 'uid': uid}
    response = client.post(
        path=reverse('api:v1:auth_app:reset-password-validate'),
        data=payload
    )

    assert response.status_code == status.HTTP_200_OK
    # валидации token и uid успешно

    new_password = {
        'password_1': 'new_password3210',
        'password_2': 'new_password3210'
    }
    payload = payload | new_password
    response = client.post(
        path=reverse('api:v1:auth_app:reset-password-confirm'),
        data=payload
    )

    assert response.status_code == status.HTTP_200_OK
    # изменение пароля после валидации успешно

    payload = {
        'email': user.email,
        'password': 'new_password3210',
    }
    response = client.post(
        path=reverse('api:v1:auth_app:sign-in'),
        data=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    # sign-in после восстановления успешен
