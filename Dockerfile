FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache add \
     gcc \
     musl-dev \
     postgresql-dev

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pipenv install