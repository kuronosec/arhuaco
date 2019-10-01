# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

#!/bin/sh

# Collects evaluation results.
cat /var/lib/arhuaco/data/models/results_sys.log | gawk '{print $13}' | grep -v -e '^$' > /var/lib/arhuaco/data/models/real_accuracy.log
cat /var/lib/arhuaco/data/models/results_sys.log | gawk '{print $25}' | grep -v -e '^$' > /var/lib/arhuaco/data/models/val_real_accuracy.log
cat /var/lib/arhuaco/data/models/results_sys.log | gawk '{print $22}' | grep -v -e '^$' > /var/lib/arhuaco/data/models/val_false_pos_rate.log
