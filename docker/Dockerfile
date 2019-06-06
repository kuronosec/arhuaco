# Arhuaco: The smart security monitoring suite
FROM debian:stretch
MAINTAINER kurono kurono@arhuaco.com

LABEL container.label=arhuaco

ENV WORK_DIRECTORY=/opt/arhuaco

RUN mkdir -p $WORK_DIRECTORY

WORKDIR $WORK_DIRECTORY

COPY ./arhuaco /opt/arhuaco/arhuaco
COPY ./requirements.txt /opt/arhuaco
COPY ./setup.py /opt/arhuaco

# Installing prerequisites.
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev python-virtualenv
RUN apt-get install -y python3-numpy
RUN apt-get install -y python3-pandas

RUN pip3 install -r ./requirements.txt

RUN apt-get install -y python3-yaml
RUN apt-get install -y sysdig
RUN apt-get install -y bro bro-common

# Install Arhuaco
RUN python3 ./setup.py install
