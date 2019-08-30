from __future__ import print_function

import os
import sys, getopt
import numpy as np
import time

from arhuaco.graphics.plot import Plot

def main(argv):
    # my_results()
    my_second_results()
    # daniel_first_results()
    # daniel_second_results()

def my_results():
    linux_total = np.fromfile("/var/lib/arhuaco/data/performance/sysdig_total_final.log",
                              dtype=float, sep="\n")
    docker_total = np.fromfile("/var/lib/arhuaco/data/performance/docker_total_final.log",
                              dtype=float, sep="\n")
    sysdig_total = np.fromfile("/var/lib/arhuaco/data/performance/linux_total_final.log",
                              dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Linux job vs docker job vs docker+sysdig job
    plot.history2error([linux_total,
                       docker_total,
                       sysdig_total],
                       [linux_total,
                       docker_total,
                       sysdig_total],
                      ['Linux',
                       'Docker',
                       'Arhuaco isolation and monitoring'],
                       "Performance test",
                       "Number of ALICE grid jobs in parallel",
                       "Average runtime [s]",
                       "/var/lib/arhuaco/data/performance/performance-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 1, 10], [ 0, 60000])

def my_second_results():
    # average
    linux_total_avg = np.fromfile("/var/lib/arhuaco/data/performance/linux_avg_final.log",
                                  dtype=float, sep="\n")
    docker_total_avg = np.fromfile("/var/lib/arhuaco/data/performance/docker_avg_final.log",
                                   dtype=float, sep="\n")
    sysdig_total_avg = np.fromfile("/var/lib/arhuaco/data/performance/sysdig_avg_final.log",
                                   dtype=float, sep="\n")
    # standard deviation
    linux_total_std = np.fromfile("/var/lib/arhuaco/data/performance/linux_std_final.log",
                              dtype=float, sep="\n")
    docker_total_std = np.fromfile("/var/lib/arhuaco/data/performance/docker_std_final.log",
                              dtype=float, sep="\n")
    sysdig_total_std = np.fromfile("/var/lib/arhuaco/data/performance/sysdig_std_final.log",
                              dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Linux job vs docker job vs docker+sysdig job
    plot.history2error([linux_total_avg,
                       docker_total_avg,
                       sysdig_total_avg],
                       [linux_total_std,
                       docker_total_std,
                       sysdig_total_std],
                      ['Linux',
                       'Docker',
                       'Arhuaco isolation and monitoring'],
                       "Performance test",
                       "Number of ALICE grid jobs in parallel",
                       "Average runtime [s]",
                       "/var/lib/arhuaco/data/performance/performance-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0.5, 10.5], [ 4200, 5800])

def daniel_first_results():
    linux_total = np.fromfile("/var/lib/arhuaco/data/performance/daniel_no_hard_native.log",
                              dtype=float, sep="\n")
    docker_total = np.fromfile("/var/lib/arhuaco/data/performance/daniel_no_hard_docker.log",
                              dtype=float, sep="\n")
    rkt_total    = np.fromfile("/var/lib/arhuaco/data/performance/daniel_no_hard_rkt.log",
                              dtype=float, sep="\n")
    singul_total = np.fromfile("/var/lib/arhuaco/data/performance/daniel_no_hard_sing.log",
                              dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Linux job vs docker job vs docker+sysdig job
    plot.history2plot([linux_total,
                       docker_total,
                       rkt_total,
                       singul_total],
                      ['Linux',
                       'Docker',
                       'Rkt',
                       'Singularity'],
                       "Stock Kernel",
                       "Number of simultaneous Jobs",
                       "Average runtime [s]",
                       "/var/lib/arhuaco/data/performance/performance-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0.5, 10.5], [ 4200, 5800])

def daniel_second_results():
    linux_total = np.fromfile("/var/lib/arhuaco/data/performance/daniel_hard_native.log",
                              dtype=float, sep="\n")
    rkt_total    = np.fromfile("/var/lib/arhuaco/data/performance/daniel_hard_rkt.log",
                              dtype=float, sep="\n")
    singul_total = np.fromfile("/var/lib/arhuaco/data/performance/daniel_hard_singularity.log",
                              dtype=float, sep="\n")
    # Graphically plot the results
    plot = Plot()
    # Linux job vs docker job vs docker+sysdig job
    plot.history2plot([linux_total,
                       rkt_total,
                       singul_total],
                      ['Linux',
                       'Rkt',
                       'Singularity'],
                       "Hardened Kernel",
                       "Number of simultaneous Jobs",
                       "Average runtime [s]",
                       "/var/lib/arhuaco/data/performance/performance-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       'lower right',
                       [ 0.5, 10.5], [ 4200, 6100])

if __name__ == "__main__":
   main(sys.argv[1:])
