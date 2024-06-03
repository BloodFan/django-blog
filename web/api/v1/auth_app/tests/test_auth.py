import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
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


@email_settings
def test_register_user(client):
    """Интеграционный тест."""
    payload = {
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'email': 'test_user_email@mail.com',
        'password_1': 'test_password3210',
        'password_2': 'test_password3210',
        'birthday': '2000-01-01',
        'gender': '1',
    }

    response = client.post(
        path=reverse('api:v1:auth_app:sign-up'),
        data=payload,
    )
    print(f'{response.status_code=}')
    assert response.status_code == status.HTTP_201_CREATED
    # пользователь создан
    user = User.objects.get(email=payload['email'])
    assert user.is_active is False
    # после создания пользователь неактивен
    assert len(mail.outbox) == 1
    # после создания письмо отправлено
    payload = {
        'email': 'test_user_email@mail.com',
        'password': 'test_password3210',
    }
    response = client.post(
        path=reverse('api:v1:auth_app:sign-in'),
        data=payload,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # попытка sign in при неактивном пользователе возвращает 400

    # print(f'{mail.outbox[0].__dict__=}')
    # for key, value in mail.outbox[0].__dict__.items():
    #     print(f'{key} - {value}')

    # re.findall находит все совпадения, выводит лист
    # находит все совпадения, ограниченные:
    # начало выражения: (?<=key=), key= это символы начала объекта поиска
    # обьект поиска, все символы внутри .+
    # конец выражения (?="), " это символ конца объекта поиска

    string = mail.outbox[0].alternatives[0][0]
    key = re.findall(r'(?<=key=).+(?=")', string)[0]
    confirm = {'key': key}
    response = client.post(
        path=reverse('api:v1:auth_app:confirm'),
        data=confirm,
    )
    assert response.status_code == status.HTTP_201_CREATED
    # post-запрос confirm по ключу из email успешен
    user = User.objects.get(email=payload['email'])
    assert user.is_active is True
    # после post-запроса confirm пользователь активен
    payload = {
        'email': 'test_user_email@mail.com',
        'password': 'test_password3210',
    }
    response = client.post(
        path=reverse('api:v1:auth_app:sign-in'),
        data=payload,
    )
    assert response.status_code == status.HTTP_200_OK
    # sign-in после confirm успешен


@pytest.mark.parametrize(
    'payload, expected_status',
    (
        ({'email': 'test_email@mail.com', 'password': 'test_password3210'}, status.HTTP_200_OK),
        (
            {'email': 'test_email@mail.com', 'password': 'test_password'},
            status.HTTP_400_BAD_REQUEST,
        ),  # password does not match fixture
        (
            {'email': 'test_email_2@mail.com', 'password': 'test_password3210'},
            status.HTTP_400_BAD_REQUEST,
        ),  # email does not match fixture
    ),
)
def test_login_user(client, user, payload, expected_status):
    """test authentication procedure"""
    response = client.post(path=reverse('api:v1:auth_app:sign-in'), data=payload, follow=True)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'payload, expected_status',
    (
        ({'email': 'test_password@mail.com', 'password': 'test_password3210'}, status.HTTP_400_BAD_REQUEST),
        (
            {'email': 'test_password@mail.com', 'password': 'test_password'},
            status.HTTP_400_BAD_REQUEST,
        ),  # password does not match fixture
    ),
)
def test_login_inactive_user(client, user_inactive, payload, expected_status):
    """test authentication procedure with inactive_user"""
    response = client.post(path=reverse('api:v1:auth_app:sign-in'), data=payload, follow=True)
    assert response.status_code == expected_status


# Юнит тесты Аутентификации
# Аутентификации - процедура проверки подлинности
# Авторизация - предоставление  прав на выполнение определенных действий


@pytest.mark.parametrize(
    'payload, expected_status',
    (
        (
            {
                'first_name': 'Lion',
                'last_name': 'El jonson',
                'email': 'Dark_Angel@mail.com',
                'password_1': 'test_password3210',
                'password_2': 'test_password3210',
                'birthday': '2000-01-01',
                'gender': '1',
            },
            status.HTTP_201_CREATED,
        ),
        (
            {
                'first_name': '',
                'last_name': 'El jonson',
                'email': 'Dark_Angel@mail.com',
                'password_1': 'test_password3210',
                'password_2': 'test_password3210',
            },
            status.HTTP_400_BAD_REQUEST,
        ),  # without first_name
        (
            {
                'first_name': 'Lion',
                'last_name': '',
                'email': 'Dark_Angel@mail.com',
                'password_1': 'test_password3210',
                'password_2': 'test_password3210',
            },
            status.HTTP_400_BAD_REQUEST,
        ),  # without last_name
        (
            {
                'first_name': 'Lion',
                'last_name': 'El jonson',
                'email': '',
                'password_1': 'test_password3210',
                'password_2': 'test_password3210',
            },
            status.HTTP_400_BAD_REQUEST,
        ),  # without email
        (
            {
                'first_name': 'Lion',
                'last_name': 'El jonson',
                'email': 'Dark_Angel@mail.com',
                'password_1': '',
                'password_2': 'test_password3210',
            },
            status.HTTP_400_BAD_REQUEST,
        ),  # without password_1
        (
            {
                'first_name': 'Lion',
                'last_name': 'El jonson',
                'email': 'Dark_Angel@mail.com',
                'password_1': 'test_password3210',
                'password_2': '',
            },
            status.HTTP_400_BAD_REQUEST,
        ),  # without password_2
        (
            {
                'first_name': 'Lion',
                'last_name': 'El jonson',
                'email': 'Dark_Angel@mail.com',
                'password_1': 'test_password3210',
                'password_2': 'test_password',
            },
            status.HTTP_400_BAD_REQUEST,
        ),  # different passwords
    ),
)
@email_settings
def test_sign_up(client, user, payload, expected_status):
    """test authentication procedure"""
    response = client.post(path=reverse('api:v1:auth_app:sign-up'), data=payload, follow=True)
    assert response.status_code == expected_status
