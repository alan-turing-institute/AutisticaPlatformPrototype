FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
RUN apk --no-cache add \
     gcc \
     musl-dev \
     postgresql-dev

RUN mkdir /code
WORKDIR /code
