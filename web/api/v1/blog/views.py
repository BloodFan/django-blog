from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.v1.blog.filters import ArticleFilter

from . import serializers
from .permissions import IsAuthorOrReadOnly
from .services import BlogService
from main.pagination import BasePageNumberPagination


class ArticleViewSet(ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = BasePageNumberPagination
    filterset_class = ArticleFilter
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogService().get_active_articles(self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ArticleSerializer
        elif self.action == 'create':
            return serializers.CreateArticleSerializer
        elif self.action == 'partial_update':
            return serializers.ArticteUpdateSerializer
        return serializers.FullArticleSerializer

    # вариант вывода комментов через action
    # @action(
    #         methods=('get',),
    #         detail=True,
    #         url_path='comments'
    # )
    # def comment_list(self, request, slug):
    #     if request.method == 'GET':
    #         queryset = BlogService.comment_queryset(slug)
    #         serializer = serializers.CommentSerializer(queryset, many=True)
    #         return Response(serializer.data)


class TagViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogService.tag_queryset()

    def get_serializer_class(self):
        return serializers.TagSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogService.category_queryset()

    def get_serializer_class(self):
        return serializers.CategorySerializer


class CommentViewSet(ModelViewSet):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return BlogService().comment_queryset(self.kwargs['slug'], self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CommentSerializer
        elif self.action == 'create':
            return serializers.CommentCreateSerializer
