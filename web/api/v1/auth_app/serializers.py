from datetime import date

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.v1.auth_app.services import AuthAppService

User = get_user_model()

error_messages = {
    'not_verified': _('Email not verified'),
    'not_active': _('Your account is not active. Please contact Your administrator'),
    'wrong_credentials': _('Entered email or password is incorrect'),
    'already_registered': _('User is already registered with this e-mail address'),
    'password_not_match': _('The two password fields did not match'),
    'incorrect_birthday': _('date of birth is incorrect'),
}


class PasswordConfirmSerializer(serializers.Serializer):
    key = serializers.CharField(min_length=1)

    def validate_key(self, key: str) -> str:
        if len(key) == 0:
            raise serializers.ValidationError(
                'Error: Отсутствует или переименован key'
            )
        return key


class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)
    email = serializers.EmailField()
    gender = serializers.CharField()
    birthday = serializers.DateField()
    password_1 = serializers.CharField(write_only=True, min_length=8)
    password_2 = serializers.CharField(write_only=True, min_length=8)

    def validate_password_1(self, password: str):
        validate_password(password)
        return password

    def validate_email(self, email: str) -> str:
        if AuthAppService.is_user_exist(email):
            raise serializers.ValidationError({'email': error_messages['already_registered']})
        return email

    def validate_birthday(self, birthday):
        if date.today() <= birthday:
            raise serializers.ValidationError({'birthday': error_messages['incorrect_birthday']})
        return birthday

    def validate(self, data: dict):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError({'password_2': error_messages['password_not_match']})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, data: dict):
        email = data.get('email')
        password = data.get('password')
        user = self.authenticate(email=email, password=password)
        if not user:
            user = AuthAppService.get_user(email)
            if not user:
                msg = {'email': error_messages['wrong_credentials']}
                raise serializers.ValidationError(msg)
            if not user.is_active:
                msg = {'email': error_messages['not_active']}
                raise serializers.ValidationError(msg)
            msg = {'email': error_messages['wrong_credentials']}
            raise serializers.ValidationError(msg)
        data['user'] = user
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetValidateSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()


class PasswordResetConfirmSerializer(PasswordResetValidateSerializer):
    """Наследует от сериализатора валидации"""
    password_1 = serializers.CharField(min_length=8, max_length=64)
    password_2 = serializers.CharField(min_length=8, max_length=64)

    def validate_password_1(self, password: str):
        uid = self.initial_data['uid']
        user = AuthAppService.get_user_from_uid(uid)
        validate_password(password, user)
        return password

    def validate(self, data: dict):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError({'password_2': error_messages['password_not_match']})
        return data
