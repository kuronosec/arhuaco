# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

#!/bin/sh

PYTHON_COMMAND="python3"

$PYTHON_COMMAND test_compare_svm_conv.py -t syscall >> /var/lib/arhuaco/data/models/results_sys.log &
$PYTHON_COMMAND test_compare_svm_conv.py -t network >> /var/lib/arhuaco/data/models/results_net.log &
