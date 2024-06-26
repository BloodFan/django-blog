from typing import TYPE_CHECKING

from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

if TYPE_CHECKING:
    from rest_framework.request import Request


class TemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    swagger_schema = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name: str = ''

    def get(self, request: 'Request', *args, **kwargs):
        return Response()
