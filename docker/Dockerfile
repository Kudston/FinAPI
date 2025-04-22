FROM python:3.9-slim-bullseye

RUN apt-get update -y && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/fin-api
RUN mkdir /usr/src/fin-api/requirements

COPY ./../src/requirements.txt /usr/src/fin-api/requirements/prod.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install -r /usr/src/fin-api/requirements/prod.txt

ADD . /usr/src/fin-api/
WORKDIR /usr/src/fin-api/

EXPOSE 8000