from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy
from transliterate import translit

from actions.models import Like

from .choices import ArticleStatus

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-id',)

    def save(self, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwargs)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='article_set')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='article_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ArticleStatus.choices, default=ArticleStatus.INACTIVE)
    image = models.ImageField(upload_to='articles/', blank=True, default='no-image-available.jpg')
    objects = models.Manager()
    tags = models.ManyToManyField(
        'Tag',
        db_index=True,
        through='TagArticle',
        verbose_name='Тег',
        help_text='Укажите теги',
    )
    likes = GenericRelation(Like)

    @property
    def short_title(self):
        return self.title[:30]

    def __str__(self):
        return '__str__ {title} - {author}'.format(title=self.short_title, author=self.author)
        # return '__str__ Все теги article: '+', '.join([tag.name for tag in self.tags.all()])

    def save(self, **kwargs):
        if not self.slug:
            slug = translit(self.title, 'ru', reversed=True)
            self.slug = slugify(slug)
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse_lazy('blog:blog-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-updated', '-created', 'id')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment_set', blank=True)
    content = models.TextField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    likes = GenericRelation(Like)

    objects = models.Manager()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self) -> str:
        return self.content


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега.',
        unique=True,
        help_text='Укажите название тега.',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='slug тега.',
        help_text='Введите уникальный slug.',
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('blog:tag-detail', kwargs={'slug': self.slug})


class TagArticle(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagarticles', verbose_name='tag')

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='tagarticles', verbose_name='article')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'article tag'
        verbose_name_plural = 'article tags'
        constraints = [models.UniqueConstraint(fields=['article', 'tag'], name='unique_tag_in_article')]

    def __str__(self) -> str:
        return f'{self.tag} for {self.article}.'
