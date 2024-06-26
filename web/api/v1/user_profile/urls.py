from django.urls import path

from .views import ChangePasswordAPIView, ProfileAPIView, UpdateImageAPIView, UserList, UserProfile

app_name = 'user-profile'

urlpatterns = [
    path('own-profile/', ProfileAPIView.as_view(), name='own-profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('image/', UpdateImageAPIView.as_view(), name='update-image'),
    path('profile/<int:id>/', UserProfile.as_view(), name='profile'),
    path('users-list/', UserList.as_view(), name='users-list'),
]
