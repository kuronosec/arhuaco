#!/bin/bash

PYTHON_COMMAND="python3"
ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco"

$PYTHON_COMMAND "$ARHUACO_LOCATION"/training/train_rnn_gen.py -t $1 2>> /var/log/arhuaco/training-arhuaco.log
