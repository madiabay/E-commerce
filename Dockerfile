FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -qqy update && apt-get -qqy install gettext

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY ./start.django.sh /start-django

RUN chmod +x /start-django

ADD . /app/
