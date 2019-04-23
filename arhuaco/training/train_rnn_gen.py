from __future__ import print_function

import os
import sys, getopt

import numpy as np
from arhuaco.analysis.features.data_helpers import DataHelpers
from arhuaco.analysis.generative.rnn_gen import RnnGen

def main(argv):
    type = ""
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
    except getopt.GetoptError:
       print("test_rnn_gen.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("test_rnn_gen.py -t <type>")
          sys.exit()
       elif opt in ("-t", "--type"):
          type = arg
    if type == "syscall":
        analyze_syscalls()
    elif type == "network":
        analyze_network()

def analyze_syscalls():
    # Parameters
    max_length = 10
    n_gram = 5
    sequence_length = max_length*n_gram
    maxlen = 40
    step = 3
    num_epochs = 100
    num_chars = 100
    number_samples = 1000
    seed = 5

    paths = [ "/home/data/normal_clean.csv",
              "/home/data/malicious_clean.csv"]
    labels = [ 0, 1 ]
    # Create objects
    # Create objects
    data_helpers = DataHelpers( paths, labels,
                                max_length, n_gram,
                                number_samples, seed)
    cnn_w2v = RnnGen(data_helpers, maxlen, step,
                     num_epochs, num_chars)
    cnn_w2v.get_data()
    cnn_w2v.build_model()
    cnn_w2v.train_model()

def analyze_network():
    # Parameters
    # Max words per line
    max_number_words = 5
    # Number of line per object
    n_gram = 1
    # Number of characters for data input
    max_chars_len = 40
    # Number of steps ahead to learn
    step = 1

    # Number of iterations over the data
    num_epochs = 2
    # Size of the vocabulary
    num_chars = 100
    # Consecutive samples per data extraction
    number_samples = 100000
    # Number of extractions
    samples_per_epoch = 10
    # Number of characters to generate
    number_generated = 20000
    # seed for random operations
    seed = 4
    paths = [ "/home/data/dns_normal.log",
              "/home/data/dns_malicious.log"]
    labels = [ -1, 1 ]
    weights_file = "/home/data/models/gen_model.weights"
    model_file   = "/home/data/models/gen_model.json"
    generated_file = "/home/data/models/generated"

    # Create objects
    data_helpers = DataHelpers( paths, labels,
                                max_number_words, n_gram,
                                number_samples, seed)
    cnn_w2v = RnnGen(data_helpers=data_helpers,
                     maxlen=max_chars_len,
                     step=step, num_epochs=num_epochs,
                     num_chars=num_chars,
                     samples_per_epoch=samples_per_epoch,
                     weights_file=weights_file,
                     model_file=model_file,
                     generated_file=generated_file,
                     number_generated=number_generated)

    cnn_w2v.get_data()
    cnn_w2v.build_model()
    cnn_w2v.train_model()

if __name__ == "__main__":
   main(sys.argv[1:])
