from django.urls import path

from main.views import TemplateAPIView

urlpatterns = [
    path('newsline/', TemplateAPIView.as_view(template_name='newsline/newsline.html'), name='newsline'),
]