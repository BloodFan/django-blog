from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from blog.models import Article, Tag


class ListCharFilter(filters.BaseInFilter, filters.CharFilter):
    """Filter for django-filter lib
    ListCharFilter return: list[str]
    filters.CharFilter return: str
    """

    pass


class ArticleFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    tags = ListCharFilter(method='tags_filter')
    # tags = ListCharFilter(field_name='tags', lookup_expr='in') альт для tags, допустимо field_name='tags__id'
    author = filters.CharFilter(method='author_filter')
    # author = filters.CharFilter(field_name='author__email') альт синтаксис для author

    class Meta:
        model = Article
        fields = []

    # article, где есть ВСЕ требуемые теги, пока нигде не используется
    # articles/?multiple_tags=youtube&multiple_tags=Django
    multiple_tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    def search_filter(self, queryset, name, value):
        '''/article/articles/?search=test'''
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def tags_filter(self, queryset: QuerySet[Article,], name: str, value: list[str]):
        '''
        article/articles/?tags=1,2
        возвращает Article, в который есть хоть один тег из списка(OR)
        '''
        return queryset.filter(Q(tags__in=value))

    def author_filter(self, queryset, name, value):
        '''?author=test@test.com'''
        return queryset.filter(Q(author__email=value))
