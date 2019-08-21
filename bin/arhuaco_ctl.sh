#!/bin/bash

if [ "$1" == "python2.7" ]
then
    echo "Arhuaco with python2.7 starting..."
    PYTHON_COMMAND="/usr/bin/python"
    ARHUACO_LOCATION="/usr/local/lib/python2.7/dist-packages/arhuaco/"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
elif [ "$1" == "python3" ]
then
    echo "Arhuaco with python3 starting..."
    PYTHON_COMMAND="/usr/bin/python3.4"
    ARHUACO_LOCATION="/usr/local/lib/python3.4/dist-packages/arhuaco/"
    sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
elif [ "$1" == "kill" ]
then
    echo "Killing arhuaco..."
    sudo /usr/bin/python3.4 /usr/local/lib/python3.4/dist-packages/arhuaco/service/arhuaco_daemon.py stop
    sudo /opt/bro/bin/broctl stop
    sudo killall tail python python3.4 sysdig bro aliroot
    sudo rm /var/log/arhuaco/arhuaco.pid
else
    echo "Usage: arhuaco.sh [python2.7/python3/kill]"
fi

if [ "$2" == "debug" ]
then
   sudo $PYTHON_COMMAND "$ARHUACO_LOCATION"/test/main.py
fi
