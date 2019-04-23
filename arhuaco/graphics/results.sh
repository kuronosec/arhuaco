#!/bin/sh

cat /home/data/models/results_sys.log | gawk '{print $13}' | grep -v -e '^$' > /home/data/models/real_accuracy.log
cat /home/data/models/results_sys.log | gawk '{print $25}' | grep -v -e '^$' > /home/data/models/val_real_accuracy.log
cat /home/data/models/results_sys.log | gawk '{print $22}' | grep -v -e '^$' > /home/data/models/val_false_pos_rate.log
