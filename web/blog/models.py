from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from . import managers
from .choices import ArticleStatus

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='article_set')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='article_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ArticleStatus.choices, default=ArticleStatus.INACTIVE)

    objects = models.Manager()

    @property
    def short_title(self):
        return self.title[:30]

    def __str__(self):
        return '{title} - {author}'.format(title=self.short_title, author=self.author)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-updated', '-created', 'id')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_set')
    content = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')