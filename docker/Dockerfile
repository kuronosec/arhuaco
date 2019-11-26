# Arhuaco: The smart security monitoring suite
FROM debian:stretch
MAINTAINER kurono kurono@riseup.net

LABEL container.label=arhuaco

ENV WORK_DIRECTORY=/opt/arhuaco
ENV LOG_DIRECTORY=/var/log/arhuaco

RUN mkdir -p $WORK_DIRECTORY
RUN mkdir -p $LOG_DIRECTORY

WORKDIR $WORK_DIRECTORY

COPY ./ /opt/arhuaco/
# COPY ./requirements.txt /opt/arhuaco
# COPY ./setup.py /opt/arhuaco
# COPY ./bin /opt/arhuaco/bin

# Install prerequisites.
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev python-virtualenv
# Install pip requirememts.
RUN pip3 install -r ./requirements.txt

RUN apt-get install -y python3-yaml
RUN apt-get install -y sysdig procps
RUN apt-get install -y bro bro-common broctl
RUN broctl deploy
RUN apt-get install nano mlocate

# Install Arhuaco.
RUN python3 ./setup.py install
