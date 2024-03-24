from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth_app.urls')),
    path('article/', include('api.v1.blog.urls')),
    path('contact/', include('api.v1.contact_us.urls')),
    path('user-profile/', include('api.v1.user_profile.urls')),
    path('actions/', include('api.v1.actions.urls')),
    path('chat/', include('api.v1.chat.urls')),
]
