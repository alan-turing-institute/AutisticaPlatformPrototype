release: pipenv install --three --deploy --ignore-pipfile && source /root/.local/share/virtualenvs/code-_Py8Si6I/bin/activate && python manage.py migrate --noinput
web: gunicorn main_app.wsgi --log-file=-
