#!/bin/sh


echo xxx3
echo $DATABASE
echo xxx4

pipenv run python manage.py migrate
pipenv run python manage.py runserver 0.0.0.0:8000

exec "$@"