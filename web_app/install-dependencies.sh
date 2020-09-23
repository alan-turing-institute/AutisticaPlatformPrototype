#!/bin/sh

python -m pip install --upgrade pip
pip install -r requirements.txt
pipenv install

exec "$@"