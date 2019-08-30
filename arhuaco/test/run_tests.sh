#!/bin/sh

PYTHON_COMMAND="/home/andres/development/tests/keras_old/bin/python"

$PYTHON_COMMAND test_compare_svm_conv.py -t syscall >> /var/lib/arhuaco/data/models/results_sys.log &
$PYTHON_COMMAND test_compare_svm_conv.py -t network >> /var/lib/arhuaco/data/models/results_net.log &
