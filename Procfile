release: pipenv install --three --deploy --ignore-pipfile && python manage.py migrate --noinput
web: gunicorn main_app.wsgi --log-file=-
