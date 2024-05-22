from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .choices import ActionEvent

User = get_user_model()


class Like(models.Model):
    class Vote(models.IntegerChoices):
        LIKE = 1
        DISLIKE = 0

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    vote = models.PositiveSmallIntegerField(choices=Vote.choices)
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # тип связанной модели
    object_id = models.PositiveIntegerField()  # id связанной модели
    content_object = GenericForeignKey()  # сам обьект


class Following(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-id',)
        # indexes = [models.Index(fields=['author', 'user'])] для создания индекса по 2+ полям модели
        constraints = [
            models.UniqueConstraint(fields=('user', 'author'), name='unique_following'),  # связь user-author уникальна
            models.CheckConstraint(  # условие: user != author
                check=~models.Q(user=models.F('author')), name='unique_sql_following'
            ),
        ]


class Action(models.Model):
    event = models.CharField(choices=ActionEvent.choices, max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    meta = models.JSONField(blank=True, null=True, default=dict)
    content_object = GenericForeignKey()

    class Meta:
        ordering = ('-date',)


class ActionUsers(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Action Users"
        constraints = [models.UniqueConstraint(fields=('user', 'action'), name='unique_familiarization')]
