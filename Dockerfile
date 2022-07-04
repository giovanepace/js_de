ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.9.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

# FROM datamechanics/spark:3.0.1-hadoop-3.2.0-java-11-scala-2.12-python-3.8-latest

# ENV PYSPARK_MAJOR_PYTHON_VERSION = 3

# WORKDIR /opt/application

# USER root
RUN apt-get update \
 && apt-get install wget unzip zip -y

RUN mkdir /tmp/jars/

RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.22.jar
RUN mv postgresql-42.2.22.jar /tmp/jars/

ENV PYSPARK_SUBMIT_ARGS="--jars /tmp/jars/postgresql-42.2.22.jar --driver-class-path /tmp/jars/postgresql-42.2.22.jar pyspark-shell"

COPY ./app .
COPY ./entrypoint.sh .
COPY ./requirements.txt .

RUN chmod +x ./entrypoint.sh

RUN pip3 install -r requirements.txt 

ENTRYPOINT ["./entrypoint.sh"]