FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /webapps
WORKDIR /webapps
RUN pip install -U pip setuptools
RUN pip install --upgrade pip
ADD requirements.txt /webapps/
RUN pip install -r requirements.txt
ADD . /webapps/
# Django service
EXPOSE 8000
## THE LIFE SAVER
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
## Launch the wait tool and then your application
CMD /wait