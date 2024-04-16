from django.urls import path

from .views import (ChatUserAPIView, ValidateInitChatUserAPIView,
                    UserDataByJWTAPIView, UserDataByIdAPIView)

app_name = 'chat'

urlpatterns = [
    path('users/', ChatUserAPIView.as_view(), name='users'),
    path('init-chat/', ValidateInitChatUserAPIView.as_view(), name='init_chat'),
    path('user-data-by-jwt/', UserDataByJWTAPIView.as_view(), name='user_data_by_jwt'),
    path('user-data-by-id/', UserDataByIdAPIView.as_view(), name='user_data_by_id'),
]
