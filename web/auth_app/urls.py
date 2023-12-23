from django.urls import path
from django.views.generic import TemplateView

from main.views import TemplateAPIView

app_name = 'auth_app'


urlpatterns = [

    path(
        'confirm_reset_password/',
        TemplateAPIView.as_view(template_name='auth_app/confirm_reset_password.html'),
        name='confirm_reset_password'
    ),
    path('confirm/', TemplateAPIView.as_view(template_name='auth_app/confirm.html'), name='confirm'),
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'password-recovery/',
        TemplateAPIView.as_view(template_name='auth_app/reset_password_sent.html'),
        name='reset_email_sent',
    ),
    path('verify-email/', TemplateView.as_view(), name='account_verification'),
]
