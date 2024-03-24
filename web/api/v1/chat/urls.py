from django.urls import path

from .views import ChatUserAPIView, ValidateChatUserAPIView, ValidateJWTAPIView, UserDataByIdAPIView

app_name = 'chat'

urlpatterns = [
    path('users/', ChatUserAPIView.as_view(), name='users'),
    path('confirm-users/', ValidateChatUserAPIView.as_view(), name='validate_chat_user'),
    path('validate-jwt/', ValidateJWTAPIView.as_view(), name='validate_jwt'),
    path('user-data-by-id/', UserDataByIdAPIView.as_view(), name='user_data_by_id'),
]
