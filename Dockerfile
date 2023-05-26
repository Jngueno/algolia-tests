FROM apache/airflow:2.6.1

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=linux \
    AIRFLOW_GPL_UNIDECODE=yes

RUN apt-get -y update \
 && apt-get -y install python3 python3-pip libpq-dev postgresql-client python3-dev python3-distutils

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
