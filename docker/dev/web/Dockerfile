FROM python:3.11-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1 \
    # Сохранение байт-кода ?
    PYTHONUNBUFFERED=1 \
    # потоки stdout и stderr, отправляются прямо на терминал 
    TZ=Europe/Kiev \
    LANG=C.UTF-8 \
    APP_HOME=/usr/src/web  
    # APP_HOME переменная для дальнейшего использования

WORKDIR $APP_HOME

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apk add --update --no-cache curl postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev build-base \
    # install Pillow dependencies
    # apk — это система пакетов Alpine Linux
    # --update
    # --no-cache - не использовать cache данные, чистый образ
    # curl - передачи данных с помощью URL-адресов
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev && \
    pip install --upgrade pip setuptools && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"

COPY ./web/setup.cfg ./web/pyproject.toml $APP_HOME/
COPY ./web/src/requirements  ./src/requirements
RUN pip install -e .[local]

COPY --chown=$USER:$USER ./docker/dev/web/entrypoints /
COPY --chown=$USER:$USER ./web $APP_HOME

RUN chmod +x /*.sh && \
    mkdir -p $APP_HOME/static && \
    chown -R $USER:$USER $APP_HOME

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

USER $USER
