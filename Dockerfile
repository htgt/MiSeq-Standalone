FROM ubuntu:18.04

COPY . /app
CMD python manage.py runserver 0:8000