#!/bin/bash

if [ "$1" == "python2.7" ]
then
    echo "Arhuaco sensor with python2.7 starting..."
    PYTHON_COMMAND="python"
    ARHUACO_LOCATION="/usr/local/lib/python2.7/dist-packages/arhuaco"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/service/sensor_daemon.py start
elif [ "$1" == "start" ]
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
    sudo rm /var/log/arhuaco/arhuaco.pid
else
    echo "Usage: arhuaco_sensor_ctl.sh <start/stop>"
fi
