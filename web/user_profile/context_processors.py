from django.conf import settings


def chat_url(request):
    '''Вывод переменной для URL чата'''
    return {'CHAT_URL': settings.CHAT_URL}
