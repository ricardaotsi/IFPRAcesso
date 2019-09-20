FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapps
WORKDIR /webapps
RUN apt-get update
RUN apt-get --assume-yes install postgresql-client
RUN pip install -U pip setuptools
RUN pip install --upgrade pip
ADD requirements.txt /webapps/
RUN pip install -r requirements.txt
ADD . /webapps/
# Django service
EXPOSE 8000
