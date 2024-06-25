from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import ArticleViewSet, CategoryViewSet, CommentViewSet, TagViewSet

router = DefaultRouter()

router.register('articles', ArticleViewSet, basename='articles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagViewSet, basename='tags')
# router.register('comments', CommentViewSet, basename='comments')

app_name = 'blog'

articles_router = NestedSimpleRouter(router, 'articles', lookup='article')
articles_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    # path('articles/<str:slug>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('', include(articles_router.urls)),
]

urlpatterns += router.urls
