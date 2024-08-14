#!/bin/sh

if [ "$DEBUG" = "True" ]; then
    python manage.py migrate
    python manage.py load_data_bd
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
    python manage.py collectstatic --noinput --clear
fi

gunicorn tree_menu.wsgi:application --bind 0.0.0.0:8000
