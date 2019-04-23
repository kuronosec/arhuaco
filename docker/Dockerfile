# Monitor ALICE alien Jobs from a parallel 
# container

FROM debian:jessie
MAINTAINER kurono andres.gomez@cern.ch

LABEL container.label=alien-monitoring

ENV WORK_DIRECTORY=/opt/monitor                                                                                 \
    APMON=ApMon_py_2.20.tgz

RUN     mkdir $WORK_DIRECTORY

WORKDIR $WORK_DIRECTORY

COPY opt/ApMon_py_2.20.tgz /opt/ApMon_py_2.20.tgz
COPY opt/monitor /opt/monitor

# Installing prerequisites.
RUN  apt-get update  -y                                                                                       && \
     apt-get install -y python                                                                                && \
     apt-get install -y python-pip                                                                            && \
     apt-get install -y net-tools                                                                             && \
     pip install future                                                                                       && \
     pip install docker-py                                                                                    && \
     cd /opt                                                                                                  && \
     tar -xvf $APMON                                                                                          && \
     cd  ./ApMon-2.20                                                                                         && \
     python setup.py install
