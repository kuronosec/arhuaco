#!/bin/bash

PYTHON_COMMAND="python3"
ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco"

if [ "$1" == "start" ]
then
    echo "Starting arhuaco..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_daemon.py start
elif [ "$1" == "stop" ]
then
    echo "Killing arhuaco..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_daemon.py stop
    sudo killall tail
    sudo rm /var/lib/arhuaco/arhuaco-service.pid
elif [ "$2" == "debug" ]
then
   sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
else
    echo "Usage: arhuaco_ctl.sh <start/stop/debug>"
fi
