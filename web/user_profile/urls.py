from django.urls import path

from main.views import TemplateAPIView

app_name = 'user_profile'


urlpatterns = [
    path('own-profile/', TemplateAPIView.as_view(template_name='profile/base.html'), name='own-profile'),
    path('profile/<int:id>/', TemplateAPIView.as_view(template_name='profile/userProfile.html'), name='profile'),
    path('profile/subscriptions/', TemplateAPIView.as_view(template_name='profile/subscriptions/base.html'), name='profile'),
]
