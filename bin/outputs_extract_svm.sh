#!/bin/bash

# sample:  - 3910s - loss: 0.0268 - acc: 0.9940 - false_pos_rate: 0.0074 -
# real_accuracy: 0.9940 - sensitivity: 0.9953 - specificity: 0.9926 - val_loss:
# 0.0237 - val_acc: 0.9955 - val_false_pos_rate: 0.0061 - val_real_accuracy: 0.9955
# - val_sensitivity: 0.9972 - val_specificity: 0.9939

cat /var/lib/arhuaco/data/logs/output_sys_svm.log | grep real_accuracy | gawk '{print $14}' > /var/lib/arhuaco/data/logs/sys_accuracy_svm.log
cat /var/lib/arhuaco/data/logs/output_sys_svm.log | grep real_accuracy | gawk '{print $32}' > /var/lib/arhuaco/data/logs/sys_val_accuracy_svm.log
cat /var/lib/arhuaco/data/logs/output_sys_svm.log | grep real_accuracy | gawk '{print $11}' > /var/lib/arhuaco/data/logs/sys_fpr_svm.log
cat /var/lib/arhuaco/data/logs/output_sys_svm.log | grep real_accuracy | gawk '{print $29}' > /var/lib/arhuaco/data/logs/sys_val_fpr_svm.log
cat /var/lib/arhuaco/data/logs/output_net_svm.log | grep real_accuracy | gawk '{print $14}' > /var/lib/arhuaco/data/logs/net_accuracy_svm.log
cat /var/lib/arhuaco/data/logs/output_net_svm.log | grep real_accuracy | gawk '{print $32}' > /var/lib/arhuaco/data/logs/net_val_accuracy_svm.log
cat /var/lib/arhuaco/data/logs/output_net_svm.log | grep real_accuracy | gawk '{print $11}' > /var/lib/arhuaco/data/logs/net_fpr_svm.log
cat /var/lib/arhuaco/data/logs/output_net_svm.log | grep real_accuracy | gawk '{print $29}' > /var/lib/arhuaco/data/logs/net_val_fpr_svm.log

# extract new generated data
cat /var/lib/arhuaco/data/logs/output_net_svm_generated.log | grep real_accuracy | gawk '{print $14}' > /var/lib/arhuaco/data/logs/net_acc_gen_svm.log
cat /var/lib/arhuaco/data/logs/output_net_svm_generated.log | grep real_accuracy | gawk '{print $32}' > /var/lib/arhuaco/data/logs/net_val_acc_gen_svm.log

# Show resulting files

echo "/var/lib/arhuaco/data/logs/sys_accuracy.log"
cat /var/lib/arhuaco/data/logs/sys_accuracy_svm.log
echo "/var/lib/arhuaco/data/logs/sys_val_accuracy.log"
cat /var/lib/arhuaco/data/logs/sys_val_accuracy_svm.log
echo "/var/lib/arhuaco/data/logs/sys_fpr.log"
cat /var/lib/arhuaco/data/logs/sys_fpr_svm.log
echo "/var/lib/arhuaco/data/logs/sys_val_fpr.log"
cat /var/lib/arhuaco/data/logs/sys_val_fpr_svm.log
echo "/var/lib/arhuaco/data/logs/net_accuracy.log"
cat /var/lib/arhuaco/data/logs/net_accuracy_svm.log
echo "/var/lib/arhuaco/data/logs/net_val_accuracy.log"
cat /var/lib/arhuaco/data/logs/net_val_accuracy_svm.log
echo "/var/lib/arhuaco/data/logs/net_fpr.log"
cat /var/lib/arhuaco/data/logs/net_fpr_svm.log
echo "/var/lib/arhuaco/data/logs/net_val_fpr.log"
cat /var/lib/arhuaco/data/logs/net_val_fpr_svm.log
