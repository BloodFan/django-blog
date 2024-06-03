from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import TemplateAPIView

app_name = 'blog'

router = DefaultRouter()


urlpatterns = [
    path('blog/', TemplateAPIView.as_view(template_name='blog/post_list.html'), name='blog-list'),
    path('create-blog/', TemplateAPIView.as_view(template_name='blog/post_create.html'), name='blog-create'),
    path('blog/<str:slug>/', TemplateAPIView.as_view(template_name='blog/post_detail.html'), name='blog-detail'),
    path('blog/<str:slug>/edit/', TemplateAPIView.as_view(template_name='blog/post_edit.html'), name='blog-edit'),
    path('blog/tags/<str:slug>/', TemplateAPIView.as_view(template_name='blog/tag_detail.html'), name='tag-detail'),
]

urlpatterns += router.urls
