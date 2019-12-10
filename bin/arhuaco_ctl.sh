#!/bin/bash

# This script executes the analysis service in arhuaco.
# It reads the plaon log files where the sensor has stored
# the data about the status of the system.

# Arhuaco only supports currently python 3.
PYTHON_COMMAND="python3"
# TODO: make this more generic for other versions of python 3.
ARHUACO_LOCATION="/usr/local/lib/python3.6/dist-packages/arhuaco"

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
elif [ "$1" == "REST" ]
then
    echo "Starting Arhuaco WEB service..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/arhuaco_web_service.py
elif [ "$2" == "debug" ]
then
   sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
else
    echo "Usage: arhuaco_ctl.sh <start/stop/debug>"
fi
