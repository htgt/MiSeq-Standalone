FROM ubuntu:18.04
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update -y
RUN apt-get install -y python3-pip

RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 8000
CMD python3 /app/manage.py runserver 0:8000