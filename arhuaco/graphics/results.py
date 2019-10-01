# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from __future__ import print_function

import os
import sys, getopt
import numpy as np
import time

from arhuaco.graphics.plot import Plot

# Collect and plot evaluation results

def main(argv):
    training_vs_validation_cnn()
    training_vs_validation_svm()
    comparative_results()

def training_vs_validation_cnn():
    sys_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/sys_accuracy_cnn.log",
                               dtype=float, sep="\n")
    sys_val_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_accuracy_cnn.log",
                                   dtype=float, sep="\n")
    sys_fpr = np.fromfile("/var/lib/arhuaco/data/logs/sys_fpr_cnn.log",
                          dtype=float, sep="\n")
    sys_val_fpr = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_fpr_cnn.log",
                              dtype=float, sep="\n")
    net_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/net_accuracy_cnn.log",
                               dtype=float, sep="\n")
    net_val_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/net_val_accuracy_cnn.log",
                                   dtype=float, sep="\n")
    net_fpr = np.fromfile("/var/lib/arhuaco/data/logs/net_fpr_cnn.log",
                          dtype=float, sep="\n")
    net_val_fpr = np.fromfile("/var/lib/arhuaco/data/logs/net_val_fpr_cnn.log",
                              dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Training vs validation
    plot.history2plot([sys_accuracy,
                       sys_val_accuracy],
                       ['Training', 'Validation'],
                       "System call classification with CNN", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/sys_conv_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9], [ 0.8, 1.0 ])
    plot.history2plot([sys_fpr,
                       sys_val_fpr],
                       ['Training', 'Validation'],
                       "System call classification with CNN", "Epoch", "False positive rate",
                       "/var/lib/arhuaco/data/logs/sys_conv_fpr-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])
    plot.history2plot([net_accuracy,
                       net_val_accuracy],
                       ['Training', 'Validation'],
                       "Network trace classification with CNN", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/net_conv_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9 ], [ 0.8, 1.0 ])
    plot.history2plot([net_fpr,
                       net_val_fpr],
                       ['Training', 'Validation'],
                       "Network trace classification with CNN", "Epoch", "False postive rate",
                       "/var/lib/arhuaco/data/logs/net_conv_fpr-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])

def training_vs_validation_svm():
    sys_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/sys_accuracy_svm.log",
                               dtype=float, sep="\n")
    sys_val_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_accuracy_svm.log",
                                   dtype=float, sep="\n")
    sys_fpr = np.fromfile("/var/lib/arhuaco/data/logs/sys_fpr_svm.log",
                         dtype=float, sep="\n")
    sys_val_fpr = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_fpr_svm.log",
                              dtype=float, sep="\n")
    net_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/net_accuracy_svm.log",
                               dtype=float, sep="\n")
    net_val_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/net_val_accuracy_svm.log",
                                   dtype=float, sep="\n")
    net_gen_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/net_acc_gen_svm.log",
                               dtype=float, sep="\n")
    net_gen_val_accuracy = np.fromfile("/var/lib/arhuaco/data/logs/net_val_acc_gen_svm.log",
                                   dtype=float, sep="\n")
    net_fpr = np.fromfile("/var/lib/arhuaco/data/logs/net_fpr_svm.log",
                          dtype=float, sep="\n")
    net_val_fpr = np.fromfile("/var/lib/arhuaco/data/logs/net_val_fpr_svm.log",
                              dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Training vs validation
    plot.history2plot([sys_accuracy,
                       sys_val_accuracy],
                       ['Training', 'Validation'],
                       "System call classification with SVM", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/sys_svm_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9], [ 0.8, 1.0 ])
    plot.history2plot([sys_fpr,
                       sys_val_fpr],
                       ['Training', 'Validation'],
                       "System call classification with SVM", "Epoch", "False positive rate",
                       "/var/lib/arhuaco/data/logs/sys_svm_fpr-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])
    plot.history2plot([net_accuracy,
                       net_val_accuracy],
                       ['Training', 'Validation'],
                       "Network trace classification with SVM", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/net_svm_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9 ], [ 0.8, 1.0 ])
    plot.history2plot([net_fpr,
                       net_val_fpr],
                       ['Training', 'Validation'],
                       "Network trace classification with SVM", "Epoch", "False postive rate",
                       "/var/lib/arhuaco/data/logs/net_svm_fpr-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])
    plot.history2plot([net_gen_accuracy,
                       net_gen_val_accuracy],
                       ['Training', 'Validation'],
                       "Network trace classification with SVM: generated data", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/net_svm_accuracy-generated-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9 ], [ 0.8, 1.0 ])

def comparative_results():
    sys_val_accuracy_cnn = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_accuracy_cnn.log",
                                       dtype=float, sep="\n")
    sys_val_accuracy_svm = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_accuracy_svm.log",
                                       dtype=float, sep="\n")
    sys_val_fpr_cnn = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_fpr_cnn.log",
                                  dtype=float, sep="\n")
    sys_val_fpr_svm = np.fromfile("/var/lib/arhuaco/data/logs/sys_val_fpr_svm.log",
                                  dtype=float, sep="\n")
    net_val_accuracy_cnn = np.fromfile("/var/lib/arhuaco/data/logs/net_val_accuracy_cnn.log",
                                       dtype=float, sep="\n")
    net_val_accuracy_svm = np.fromfile("/var/lib/arhuaco/data/logs/net_val_accuracy_svm.log",
                                       dtype=float, sep="\n")
    net_val_fpr_cnn = np.fromfile("/var/lib/arhuaco/data/logs/net_val_fpr_cnn.log",
                                  dtype=float, sep="\n")
    net_val_fpr_svm = np.fromfile("/var/lib/arhuaco/data/logs/net_val_fpr_svm.log",
                                  dtype=float, sep="\n")
    net_val_acc_gen_svm = np.fromfile("/var/lib/arhuaco/data/logs/net_val_acc_gen_svm.log",
                                  dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Syscall cnn vs svm acc
    plot.history2plot([sys_val_accuracy_cnn[0:10],
                       sys_val_accuracy_svm[0:10]],
                       ['CNN validation', 'SVM validation'],
                       "CNN vs SVM system call validation accuracy",
                       "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/sys_cnn_svm_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9 ], [ 0, 0.2 ])
    # Syscall cnn vs svm fpr
    plot.history2plot([sys_val_fpr_cnn[0:10],
                       sys_val_fpr_svm[0:10]],
                       ['CNN validation', 'SVM validation'],
                       "CNN vs SVM system call validation false positive rate",
                       "Epoch", "False positive rate",
                       "/var/lib/arhuaco/data/logs/sys_cnn_svm_fpr-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])
    # Network cnn vs svm acc
    plot.history2plot([net_val_accuracy_cnn[0:10],
                       net_val_accuracy_svm[0:10]],
                       ['CNN validation', 'SVM validation'],
                       "CNN vs SVM network trace validation accuracy",
                       "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/logs/net_cnn_svm_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0, 9 ], [ 0, 0.2 ])
    # Network cnn vs svm fpr
    plot.history2plot([net_val_fpr_cnn[0:10],
                       net_val_fpr_svm[0:10]],
                       ['CNN validation', 'SVM validation'],
                       "CNN vs SVM network validation false positive rate",
                       "Epoch", "False positive rate",
                       "/var/lib/arhuaco/data/logs/net_cnn_svm_fpr-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])
    # Network svm original vs svm generated acc
    plot.history2plot([net_val_accuracy_svm[0:10],
                       net_val_acc_gen_svm[0:10]],
                       ['SVM validation non generated', 'SVM validation generated'],
                       "SVM accuracy comparison: normal data vs generated data",
                       "Epoch", "False positive rate",
                       "/var/lib/arhuaco/data/logs/net_svm_accuracy-generated-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'upper left',
                       [ 0, 9 ], [ 0, 0.2 ])

if __name__ == "__main__":
   main(sys.argv[1:])
