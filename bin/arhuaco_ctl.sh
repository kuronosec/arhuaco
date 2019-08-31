#!/bin/bash

if [ "$1" == "python2.7" ]
then
    echo "Arhuaco with python2.7 starting..."
    PYTHON_COMMAND="python"
    ARHUACO_LOCATION="/usr/local/lib/python2.7/dist-packages/arhuaco/"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_daemon.py start
elif [ "$1" == "start" ]
then
    echo "Arhuaco with python3 starting..."
    PYTHON_COMMAND="python3"
    ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco/"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_daemon.py start
elif [ "$1" == "stop" ]
then
    echo "Killing arhuaco..."
    sudo python3 /usr/local/lib/python3.5/dist-packages/arhuaco/service/arhuaco_daemon.py stop
    sudo /opt/bro/bin/broctl stop
    sudo killall tail python python3 sysdig bro aliroot
    sudo rm /var/log/arhuaco/arhuaco.pid
else
    echo "Usage: arhuaco_ctl.sh <start/stop>"
fi

if [ "$2" == "debug" ]
then
   sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
fi
