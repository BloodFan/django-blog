from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.conf import settings

if TYPE_CHECKING:
    from api.v1.chat.views import ValidateJWTAPIView


class IsKeyInHeaders(BasePermission):
    """Есть ли ключ в Headers."""
    def has_permission(self, request, view: "ValidateJWTAPIView") -> bool:
        """Доступ к коллекции."""
        return (request.headers['Authorization'] == f'Token {settings.BLOG_HEADERS_PERMISSION}')
