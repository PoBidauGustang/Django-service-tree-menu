FROM python:3.12-slim as requirements-stage

WORKDIR /tmp

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.3

RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# FROM python:3.12
FROM python:3.12-slim

RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system --group app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE='tree_menu.settings'

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./tree_menu $APP_HOME

RUN sed -i 's/\r$//g'  ./entrypoint.sh && \
    chmod +x  ./entrypoint.sh

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["sh", "entrypoint.sh"]
