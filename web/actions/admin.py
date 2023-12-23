from django.contrib import admin

from .models import Like, Action


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fields = ('vote', 'user', 'content_type', 'object_id')
    list_display = ('vote', 'user', 'content_type', 'object_id')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'date')
