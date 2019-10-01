#!/bin/bash

# This script start the collection of inout data about the
# state of the system. This information is stored in plain
# log files.

# Arhuaco only supports currently python 3.
PYTHON_COMMAND="python3"
# TODO: make this more generic for other versions of python 3.
ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco"

if [ "$1" == "start" ]
then
    echo "Startng Arhuaco sensors..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/sensor_daemon.py start
elif [ "$1" == "stop" ]
then
    echo "Stoping Arhuaco sensors..."
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/sensor_daemon.py stop
    sudo broctl stop
    sudo killall sysdig
    sudo rm /var/lib/arhuaco/arhuaco-sensor.pid
else
    echo "Usage: arhuaco_sensor_ctl.sh <start/stop>"
fi
