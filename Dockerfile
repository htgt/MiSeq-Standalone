FROM ubuntu:18.04

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /app/requirements.txt

RUN mkdir -p /var/data/uploadedFiles/

RUN apt-get update -y
RUN apt-get install -y python3-pip

RUN pip3 install -r /app/requirements.txt

#COPY . /app
#WORKDIR /app
#EXPOSE 8000
#CMD python3 /app/manage.py runserver 0:8000

# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3.8-slim-buster



# Install pip requirements
#COPY requirements.txt .
#RUN python3 -m pip3 install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder: 'miseq-standalone'. Please enter the Python path to wsgi file.
CMD python3 /app/manage.py runserver 0:8000