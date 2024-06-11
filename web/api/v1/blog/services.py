from datetime import datetime
from typing import TYPE_CHECKING, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import (
    BooleanField,
    Case,
    CharField,
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Concat

from actions.choices import LikeStatus
from actions.models import Like
from blog.choices import ArticleStatus
from blog.models import Article, Category, Comment, Tag

from main import tasks

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class BlogService:
    def comment_queryset(self, slug: str, user: User) -> Comment:
        return (
            Comment.objects.filter(article__slug=slug, parent__isnull=True)
            .select_related('user')
            .prefetch_related(Prefetch('children', queryset=Comment.objects.select_related('user').all()))
            .all()
            .order_by('-updated')
            .annotate(user_like_status=self.like_annotate(user))
        )

    @staticmethod
    def category_queryset() -> Category:
        return Category.objects.all()

    def get_active_articles(self, user: User) -> Article:
        return (
            Article.objects.filter(status=ArticleStatus.ACTIVE)
            .select_related('category', 'author')
            .prefetch_related('tags')
            .annotate(
                comments_count=Count('comment_set'),
                # user_like=self.like_annotate(user), # К черту, буду проститутом!
                up_votes=self.annotate_votes_count(LikeStatus.LIKE),
                down_votes=self.annotate_votes_count(LikeStatus.DISLIKE),
                rating=ExpressionWrapper(F('up_votes') - F('down_votes'), output_field=IntegerField()),
                is_author=self.is_author(user),
            )
        )

    def is_author(self, user: User) -> Value:
        if not user.is_authenticated:
            return Value(True, output_field=BooleanField())
        return Case(When(author=user, then=Value(True)), default=Value(False), output_field=BooleanField())

    def like_annotate(self, user: User) -> Value:
        if not user.is_authenticated:
            return Value(LikeStatus.DOES_NOT_EXIST, output_field=IntegerField())
        return Case(
            When(likes__user=user, likes__vote=LikeStatus.LIKE, then=Value(LikeStatus.LIKE)),
            When(likes__user=user, likes__vote=LikeStatus.DISLIKE, then=Value(LikeStatus.DISLIKE)),
            default=Value(LikeStatus.DOES_NOT_EXIST),
            output_field=IntegerField(),
        )

    def annotate_votes_count(self, votes: int) -> Subquery:
        return Subquery(
            Article.objects.filter(id=OuterRef('id'))
            .annotate(count=Count('likes', filter=Q(likes__vote=votes)))
            .values('count')[:1]
        )

    @staticmethod
    def tag_queryset() -> Tag:
        return (
            Tag.objects.annotate(ordering_count=Count('tagarticles__article'))
            .order_by(F('ordering_count').desc())
            .all()[:8]
        )

    @staticmethod
    def send_message(user: User):
        """Письмо для пользователя о создании нового поста."""
        template_name = 'emails/create_new_blog_for_user.html'
        context = {'full_name': user.full_name, 'frontend_url': settings.FRONTEND_URL}
        subject = 'Пост создан!'

        tasks.send_information_email.delay(
            subject=subject,
            template_name=template_name,
            context=context,
            to_email=user.email,
            from_email=settings.ADMIN_EMAIL,
        )

    @staticmethod
    def send_message_for_admin(user: User, article: Article):
        """Письмо для админа о создании нового поста."""
        template_name = 'emails/create_new_blog_for_admin.html'
        context = {
            'user_full_name': user.full_name,
            'user_email': user.email,
            'url': f'{settings.FRONTEND_URL}admin/blog/article/' f'{article.id}/change/',
        }
        subject = 'Премодерация нового поста.'
        tasks.send_information_email.delay(
            subject=subject,
            template_name=template_name,
            context=context,
            to_email=settings.ADMIN_EMAIL,
            from_email=settings.ADMIN_EMAIL,
        )

    @staticmethod
    def get_user_like_status(user: User, obj: Union[Article, Comment]) -> int:
        """except если пост еще не был оценён или пользователь не авторизован."""
        try:
            like = obj.likes.get(user=user)
            return like.vote
        except (Like.DoesNotExist, TypeError):
            return LikeStatus.DOES_NOT_EXIST

    def admin_notify(self, time_period: datetime) -> Article:
        """Создано для Selery task"""
        admin = User.objects.get(email=settings.ADMIN_EMAIL)
        return (
            self.get_active_articles(admin)
            .filter(created__gte=time_period)
            .annotate(
                vote_count=ExpressionWrapper(F('up_votes') + F('down_votes'), output_field=IntegerField()),
                tags_list=ArrayAgg('tags__name', distinct=True),
            )
            .values(
                'title',
                'tags_list',
                'up_votes',
                'down_votes',
                'vote_count',
                'rating',
                'comments_count',
                category_name=F('category__name'),
                author_full_name=Concat(
                    F('author__first_name'), Value(' '), F('author__last_name'), output_field=CharField()
                ),
                author_email=F('author__email'),
            )
        )
