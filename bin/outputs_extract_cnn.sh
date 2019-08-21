#!/bin/bash

# sample:  - 3910s - loss: 0.0268 - acc: 0.9940 - false_pos_rate: 0.0074 -
# real_accuracy: 0.9940 - sensitivity: 0.9953 - specificity: 0.9926 - val_loss:
# 0.0237 - val_acc: 0.9955 - val_false_pos_rate: 0.0061 - val_real_accuracy: 0.9955
# - val_sensitivity: 0.9972 - val_specificity: 0.9939

cat /home/data/logs/output_sys_cnn.log | grep real_accuracy | gawk '{print $14}' > /home/data/logs/sys_accuracy_cnn.log
cat /home/data/logs/output_sys_cnn.log | grep real_accuracy | gawk '{print $26}' > /home/data/logs/sys_val_accuracy_cnn.log
cat /home/data/logs/output_sys_cnn.log | grep real_accuracy | gawk '{print $11}' > /home/data/logs/sys_fpr_cnn.log
cat /home/data/logs/output_sys_cnn.log | grep real_accuracy | gawk '{print $29}' > /home/data/logs/sys_val_fpr_cnn.log
cat /home/data/logs/output_net_cnn.log | grep real_accuracy | gawk '{print $14}' > /home/data/logs/net_accuracy_cnn.log
cat /home/data/logs/output_net_cnn.log | grep real_accuracy | gawk '{print $26}' > /home/data/logs/net_val_accuracy_cnn.log
cat /home/data/logs/output_net_cnn.log | grep real_accuracy | gawk '{print $11}' > /home/data/logs/net_fpr_cnn.log
cat /home/data/logs/output_net_cnn.log | grep real_accuracy | gawk '{print $29}' > /home/data/logs/net_val_fpr_cnn.log

# Show resulting files

echo "/home/data/logs/sys_accuracy.log"
cat /home/data/logs/sys_accuracy_cnn.log
echo "/home/data/logs/sys_val_accuracy.log"
cat /home/data/logs/sys_val_accuracy_cnn.log
echo "/home/data/logs/sys_fpr.log"
cat /home/data/logs/sys_fpr_cnn.log
echo "/home/data/logs/sys_val_fpr.log"
cat /home/data/logs/sys_val_fpr_cnn.log
echo "/home/data/logs/net_accuracy.log"
cat /home/data/logs/net_accuracy_cnn.log
echo "/home/data/logs/net_val_accuracy.log"
cat /home/data/logs/net_val_accuracy_cnn.log
echo "/home/data/logs/net_fpr.log"
cat /home/data/logs/net_fpr_cnn.log
echo "/home/data/logs/net_val_fpr.log"
cat /home/data/logs/net_val_fpr_cnn.log
