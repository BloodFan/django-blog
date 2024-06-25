from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

app_name = 'auth_app'

urlpatterns = [
    path('confirm/', views.ConfirmView.as_view(), name='confirm'),
    path('sing-in/', views.LoginView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('password/reset/validate/', views.PasswordResetValidateView.as_view(), name='reset-password-validate'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # создание токена
    path('token/refresh/', TokenRefreshView.as_view()),  # получение access token при предоставлении Refresh
    path('token/verify/', TokenVerifyView.as_view()),  # проверяет токен
]
