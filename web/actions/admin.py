from django.contrib import admin

from .models import Action, ActionUsers, Like


@admin.register(ActionUsers)
class ActionUsersAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fields = ('vote', 'user', 'content_type', 'object_id')
    list_display = ('vote', 'user', 'content_type', 'object_id')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'content_object', 'date')
