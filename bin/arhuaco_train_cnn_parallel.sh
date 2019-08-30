#!/bin/bash

if [ "$2" == "python2.7" ]
then
    echo "python2.7"
    PYTHON_COMMAND="/usr/bin/python"
    ARHUACO_LOCATION="/usr/local/lib/python2.7/dist-packages/arhuaco/"
else
    PYTHON_COMMAND="python3"
    ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco/"
fi

nohup $PYTHON_COMMAND "$ARHUACO_LOCATION"/training/train_cnn_w2v.py -t $1 </dev/null >/var/log/arhuaco/output.log 2>&1 &
