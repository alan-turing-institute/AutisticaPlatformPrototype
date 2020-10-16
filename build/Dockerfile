FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apk --no-cache add \
     bash \
     build-base \
     curl \
     gcc \
     gettext \
     git \
     libffi-dev \
     linux-headers \
     musl-dev \
     postgresql-dev \
     tini