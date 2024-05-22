from typing import TYPE_CHECKING

from django.conf import settings
from rest_framework.permissions import SAFE_METHODS, BasePermission

if TYPE_CHECKING:
    from api.v1.chat.views import ValidateJWTAPIView


class IsKeyInHeaders(BasePermission):
    """Есть ли ключ в Headers."""

    def has_permission(self, request, view: "ValidateJWTAPIView") -> bool:
        """Доступ к коллекции."""
        return request.headers['Authorization'] == f'Token {settings.BLOG_HEADERS_PERMISSION}'
