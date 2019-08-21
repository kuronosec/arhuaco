#!/bin/bash

if [ "$1" == "python2.7" ]
then
    echo "python2.7"
    PYTHON_COMMAND="/usr/bin/python"
    ARHUACO_LOCATION="/usr/local/lib/python2.7/dist-packages/arhuaco/"
    # PYTHON_COMMAND="/home/andres/development/tests/keras_old/bin/python"
    # ARHUACO_LOCATION="/home/andres/development/tests/keras_old/lib/python2.7/site-packages/arhuaco/"
else
    echo "python3"
    PYTHON_COMMAND="/usr/bin/python3.4"
    ARHUACO_LOCATION="/usr/local/lib/python3.4/dist-packages/arhuaco/"
    # PYTHON_COMMAND="/home/andres/development/tests/python_new/bin/python"
    # ARHUACO_LOCATION="/home/andres/development/tests/python_new/lib/python3.4/site-packages/arhuaco"
fi

nohup $PYTHON_COMMAND "$ARHUACO_LOCATION"/analysis/optimization/grid_search.py -t $1 </dev/null >/var/log/arhuaco/output.log 2>&1 &
# $PYTHON_COMMAND "$ARHUACO_LOCATION"/analysis/optimization/grid_search.py -t $1
