from typing import TypeVar

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy

from .managers import UserManager
from .choices import UserGenderStatus

UserType = TypeVar('UserType', bound='User')


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=UserGenderStatus.choices, default=UserGenderStatus.NOT_KHOWN)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True, default='no-image-available.jpg')
    following = models.ManyToManyField(to='self', through='actions.Following', related_name='followers', symmetrical=False)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    def get_absolute_url(self):
        return reverse_lazy('user_profile:profile', kwargs={'id': self.id})


    @property
    def full_name(self) -> str:
        return super().get_full_name()

    @property
    def confirmation_key(self) -> str:
        return signing.dumps(obj=self.pk)
