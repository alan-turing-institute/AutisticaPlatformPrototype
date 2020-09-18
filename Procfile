release: python manage.py migrate --noinput
web: gunicorn main_app.wsgi --log-file=-
