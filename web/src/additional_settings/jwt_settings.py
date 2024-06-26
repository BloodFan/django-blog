from datetime import timedelta
from os import environ

CORS_ALLOW_CREDENTIALS = True

REST_AUTH = {
    'TOKEN_MODEL': None,
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    'JWT_AUTH_COOKIE': 'jwt-auth',
    'USE_JWT': True,
    'SESSION_LOGIN': False,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': environ.get('SECRET_KEY', 'secret'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=2),
    'AUTH_COOKIE': 'jwt-auth',  # Имя куки для JWT токена
    'AUTH_COOKIE_REFRESH': 'refresh',  # Имя куки для refresh токена
    'AUTH_COOKIE_DOMAIN': environ.get('COOKIE_DOMAIN', '.dev.kimaykin-django.ru'),
}
