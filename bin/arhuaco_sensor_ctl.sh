#!/bin/bash

if [ "$1" == "start" ]
then
    echo "Arhuaco sensor with python3 starting..."
    PYTHON_COMMAND="python3"
    ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/sensor_daemon.py start
elif [ "$1" == "stop" ]
then
    echo "Killing Arhuaco sensor..."
    PYTHON_COMMAND="python3"
    ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/sensor_daemon.py stop
    sudo broctl stop
    sudo killall sysdig
    sudo rm /var/lib/arhuaco/arhuaco.pid
else
    echo "Usage: arhuaco_sensor_ctl.sh <start/stop>"
fi
