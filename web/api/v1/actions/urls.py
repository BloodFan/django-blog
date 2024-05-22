from django.urls import path

from . import views

app_name = 'actions'

urlpatterns = [
    path('vote/', views.LikeApiView.as_view(), name='vote'),
    path('following/', views.FollowingApiView.as_view(), name='following'),
    path('subscriber-list/', views.FollowingListAPIView.as_view(), name='subscriber-list'),
    path('news-list/', views.ActionListAPIView.as_view(), name='news-list'),
    path('familiarization/', views.ActionUsersAPIView.as_view(), name='familiarization'),
]
