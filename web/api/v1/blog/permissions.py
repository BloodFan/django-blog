from typing import TYPE_CHECKING

from django.conf import settings
from rest_framework.permissions import SAFE_METHODS, BasePermission

if TYPE_CHECKING:
    from api.v1.blog.views import ArticleViewSet


class IsAuthorOrReadOnly(BasePermission):
    """Автор или безопасные методы."""

    def has_permission(self, request, view: "ArticleViewSet"):
        """Доступ к коллекции."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Редактирование объекта."""
        return request.method in SAFE_METHODS or obj.author == request.user
