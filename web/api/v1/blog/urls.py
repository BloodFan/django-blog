from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, CategoryViewSet, CommentViewSet, TagViewSet

router = DefaultRouter()

router.register('articles', ArticleViewSet, basename='articles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagViewSet, basename='tags')
# router.register('comments', CommentViewSet, basename='comments')

app_name = 'blog'

urlpatterns = [
    path('articles/<str:slug>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
]
urlpatterns += router.urls
