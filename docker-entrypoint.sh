#!/bin/bash
set -x
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python core/celery_conf.py
python core/data_generate.py
gunicorn ne_kidaem.wsgi:application --bind 0.0.0.0:8000
