from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from main.filters import ListCharFilter
from blog.models import Article, Tag


class ArticleFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    tags = ListCharFilter(method='tags_filter')

    # Записи, где есть ВСЕ требуемые теги, пока нигде не используется
    all_tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def tags_filter(self, queryset: QuerySet[Article,], name: str, value: list[str]):
        return queryset.filter(Q(tags__in=value))
