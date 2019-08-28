#!/bin/bash

if [ "$1" == "python2.7" ]
then
    echo "python2.7"
    PYTHON_COMMAND="/usr/bin/python"
    ARHUACO_LOCATION="/usr/local/lib/python2.7/dist-packages/arhuaco/"
elif [ "$1" == "python3.6" ]
then
    echo "python3"
    PYTHON_COMMAND="/usr/bin/python3.6"
    ARHUACO_LOCATION="/usr/local/lib/python3.6/dist-packages/arhuaco/"
else
    PYTHON_COMMAND="/usr/bin/python3.5"
    ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco/"
fi

# nohup $PYTHON_COMMAND "$ARHUACO_LOCATION"/training/train_cnn_w2v.py -t $1 </dev/null >/var/log/arhuaco/output.log 2>&1 &
$PYTHON_COMMAND "$ARHUACO_LOCATION"/training/train_cnn_w2v.py -t $1 2> /var/log/arhuaco/arhuaco.log
