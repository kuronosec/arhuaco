from __future__ import print_function

import os
import sys, getopt

import numpy as np
from arhuaco.analysis.features.data_helpers import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.svm.svm_w2v import SvmW2v

from keras.models import Sequential, Model
from keras.layers import Activation, Dense, Dropout\
                         , Embedding, Flatten, Input\
                         , Merge, MaxPooling1D
from keras.optimizers import SGD

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
    except getopt.GetoptError:
       print("test_svm_w2v.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("test_svm_w2v.py -t <type>")
          sys.exit()
       elif opt in ("-t", "--type"):
          type = arg
    if type == "syscall":
        analyze_syscalls()
    elif type == "network":
        analyze_network()

def analyze_syscalls():
    # Parameters
    seed = 5
    model_variation = 'svm-non-static'

    # Model Hyperparameters
    # Max lenght of one sentence
    max_length = 7
    # Number of lines included in the
    # series
    n_gram = 6
    # Total lenght of the classification
    # object
    sequence_length = max_length*n_gram
    # Size of the vector representing each word
    embedding_dim = 20
    dropout_prob = (0.25, 0.5)
    # Number of neurons in the hidden layer
    hidden_dims = 20

    # Training parameters
    number_samples = 5
    number_samples_w2v = 10000
    num_epochs = 50
    val_split = 0.1

    # Word2Vec parameters, see train_word2vec
    # Minimum word count
    min_word_count = 6
    # Number of words that make sense in the context
    context = 10
    action = "predict"
    weights_file = "/home/data/models/weights_file"
    sentence = "process ptrace request=11(PTRACE_ATTACH)"
    # Training dataset
    paths = [ "/home/data/normal_clean.csv", "/home/data/malicious_clean.csv"]
    # Training labels
    labels = [ 0, 1 ]

    # Create objects
    data_helpers = DataHelpers( paths, labels, max_length, n_gram, number_samples)
    w2v = W2V()
    sentence_stream = data_helpers.sentence_stream(number_samples_w2v)
    params = w2v.train_word2vec_stream(sentence_stream,
                              num_features=embedding_dim,
                              min_word_count=min_word_count, context=context,
                              num_epochs=num_epochs)
    svm_w2v = SvmW2v(seed, model_variation, sequence_length, embedding_dim,
                     dropout_prob, hidden_dims, number_samples,
                     num_epochs, val_split, min_word_count, context, action, weights_file,
                     sentence, paths, labels, data_helpers)
    svm_w2v.get_data(params[0], params[1], params[2])
    svm_w2v.build_model()
    svm_w2v.train_model()

def analyze_network():
    # Parameters
    seed = 5
    model_variation = 'svm-non-static'

    # Model Hyperparameters
    # Max lenght of one sentence
    max_length = 5
    # Number of lines included in the
    # series
    n_gram = 1
    # Total lenght of the classification
    # object
    sequence_length = max_length*n_gram
    # Size of the vector representing each word
    embedding_dim = 10
    dropout_prob = (0.25, 0.5)
    # Number of neurons in the hidden layer
    hidden_dims = 10

    # Training parameters
    number_samples = 5
    number_samples_w2v = 10000
    num_epochs = 100
    val_split = 0.1

    # Word2Vec parameters, see train_word2vec
    # Minimum word count
    min_word_count = 1
    # Number of words that make sense in the context
    context = 4
    action = "predict"
    weights_file = "/home/data/models/weights_file"
    sentence = "process ptrace request=11(PTRACE_ATTACH)"
    # Training dataset
    paths = [ "/home/data/dns_normal.log", "/home/data/dns_malicious.log"]
    # Training labels
    labels = [ 0, 1 ]

    # Create objects
    data_helpers = DataHelpers( paths, labels, max_length, n_gram, number_samples)
    w2v = W2V()
    sentence_stream = data_helpers.sentence_stream(number_samples_w2v)
    params = w2v.train_word2vec_stream(sentence_stream,
                              num_features=embedding_dim,
                              min_word_count=min_word_count, context=context,
                              num_epochs=num_epochs)
    svm_w2v = svmW2v(seed, model_variation, sequence_length, embedding_dim,
                     filter_sizes, num_filters, dropout_prob, hidden_dims, number_samples,
                     num_epochs, val_split, min_word_count, context, action, weights_file,
                     sentence, paths, labels, data_helpers)
    svm_w2v.get_data(params[0], params[1], params[2])
    svm_w2v.build_model()
    svm_w2v.train_model()


if __name__ == "__main__":
   main(sys.argv[1:])
