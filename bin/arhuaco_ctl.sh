#!/bin/bash

PYTHON_COMMAND="python3"
ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco"

if [ "$1" == "start" ]
then
    echo "Starting Arhuaco..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_daemon.py start \
                         2>> /var/log/arhuaco/arhuaco.log
elif [ "$1" == "stop" ]
then
    echo "Stoping Arhuaco..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_daemon.py stop \
                         2>> /var/log/arhuaco/arhuaco.log
    sudo killall tail
    sudo rm /var/lib/arhuaco/arhuaco-service.pid
elif [ "$2" == "debug" ]
then
   sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
else
    echo "Usage: arhuaco_ctl.sh <start/stop/debug>"
fi
