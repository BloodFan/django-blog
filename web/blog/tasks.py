from datetime import datetime

from django.conf import settings
from django.core.mail import get_connection

from api.v1.blog.services import BlogService
from blog.choices import DatetimeEnum

from main import tasks
from src.celery import app


@app.task(name='hello world again!')
def new_articles_admin_notify():
    articles = BlogService().admin_notify(DatetimeEnum.CURRENT_YEAR.value)

    template_name = 'blog/messages/new_articles.html'
    context = {'articles': list(articles), 'date': datetime.now()}
    subject = 'New articles.'

    # tasks.send_information_email.apply_async(
    #     kwargs={
    #         'subject': subject,
    #         'template_name': template_name,
    #         'context': context,
    #         'to_email': settings.ADMIN_EMAIL}
    # )
    list_email = [
        settings.ADMIN_EMAIL,
    ]
    #  Захардкодено, при отправлении сообщения списку пользователей
    connection = get_connection(fail_silently=False, timeout=10)  # плюсы и минусы - урок 18

    for email in list_email:
        tasks.send_information_email(
            subject=subject, template_name=template_name, context=context, to_email=email, connection=connection
        )


# chain(add.s(1, 2), add.s(3)).apply_async() ???
