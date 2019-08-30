from __future__ import print_function

import os
import sys, getopt
import numpy as np
import time

from arhuaco.analysis.features.data_helpers\
     import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.convolutional.cnn_w2v\
     import CnnW2v
from arhuaco.graphics.plot import Plot

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
    except getopt.GetoptError:
       print("test_conv_w2v.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("test_conv_w2v.py -t <type>")
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
    model_variation = 'CNN-non-static'
    verbose = 2

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
    # Conv. Filters applied to the text
    filter_sizes = (3, 4, 5)
    # Total filters used
    num_filters = 20
    dropout_prob = (0.0, 0.0)
    # Number of neurons in the hidden layer
    hidden_dims = 20

    # Training parameters
    number_samples = 5
    samples_per_epoch = 10000
    num_epochs = 100
    val_split = 0.1

    # Word2Vec parameters, see train_word2vec
    # Minimum word count
    min_word_count = 6
    # Number of words that make sense in the context
    context = 10
    weights_file_conv = "/var/lib/arhuaco/data/models/sys_W_conv-%s"\
                         % time.strftime("%Y%m%d-%H%M%S")
    model_file_conv = "/var/lib/arhuaco/data/models/sys_model_conv-%s.json"\
                      % time.strftime("%Y%m%d-%H%M%S")
    # Training dataset
    paths = [ "/var/lib/arhuaco/data/normal_clean.csv",
              "/var/lib/arhuaco/data/malicious_clean.csv"]
    # Training labels
    labels_conv = [ 0, 1 ]

    # Create objects
    data_helpers = DataHelpers( paths, None,
                                max_length, n_gram,
                                number_samples, seed)
    w2v = W2V()
    sentence_stream = data_helpers.sentence_stream(
                                   samples_per_epoch)
    params = w2v.train_word2vec_stream(sentence_stream,
                              num_features=embedding_dim,
                              min_word_count=min_word_count,
                              context=context,
                              num_epochs=num_epochs)
    cnn_w2v = CnnW2v(seed, model_variation,
                     sequence_length, embedding_dim,
                     filter_sizes, num_filters,
                     dropout_prob, hidden_dims, number_samples,
                     num_epochs, val_split,
                     min_word_count, context, weights_file_conv,
                     model_file_conv, paths, None,
                     data_helpers, verbose)
    cnn_w2v.get_data(params[0], params[1], params[2])
    cnn_w2v.build_model()
    print("Convolutional syscall training")
    history_conv = cnn_w2v.train_model(samples_per_epoch,
                                       labels_conv)
    result = cnn_w2v.test_model(10000,
                                labels_conv,
                                max_length,
                                n_gram)
    # Graphically plot the results
    plot = Plot()
    # Training vs validation
    plot.history2plot([history_conv.history['real_accuracy'],
                       history_conv.history['val_real_accuracy']],
                       ['Training', 'Validation'],
                       "CNN accuracy", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/models/sys_cnn_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='lower right')
    # Trainning vs validation fpr
    plot.history2plot([history_conv.history['false_pos_rate'],
                       history_conv.history['val_false_pos_rate']],
                       ['Training', 'Validation'],
                       "CNN false positive rate", "Epoch",
                       "False positive rate",
                       "/var/lib/arhuaco/data/models/sys_cnn_fpr-%s.pdf"\
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='upper right')

def analyze_network():
    # Parameters
    seed = 5
    model_variation = 'CNN-non-static'

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
    # Conv. Filters applied to the text
    filter_sizes = (2, 3)
    # Total filters used
    num_filters = 3
    dropout_prob = (0.0, 0.0)
    # Number of neurons in the hidden layer
    hidden_dims = 10

    # Training parameters
    number_samples = 5
    samples_per_epoch = 1000
    num_epochs = 100
    val_split = 0.1
    verbose = 2

    # Word2Vec parameters, see train_word2vec
    # Minimum word count
    min_word_count = 1
    # Number of words that make sense in the context
    context = 4
    weights_file_conv = "/var/lib/arhuaco/data/models/net_W_conv-%s"\
                         % time.strftime("%Y%m%d-%H%M%S")
    model_file_conv = "/var/lib/arhuaco/data/models/net_model_conv-%s.json"\
                      % time.strftime("%Y%m%d-%H%M%S")
    # Training dataset
    paths = [ "/var/lib/arhuaco/data/dns_normal.log",
              #"/var/lib/arhuaco/data/dns_malicious.log"]
              "/var/lib/arhuaco/data/dns_malicious_generated.log"]
    # Training labels
    labels_conv = [ 0, 1 ]

    # Create objects
    data_helpers = DataHelpers( paths, None,
                                max_length, n_gram,
                                number_samples, seed)
    w2v = W2V()
    sentence_stream = data_helpers.sentence_stream(
                                   samples_per_epoch)
    params = w2v.train_word2vec_stream(sentence_stream,
                              num_features=embedding_dim,
                              min_word_count=min_word_count,
                              context=context,
                              num_epochs=num_epochs)
    cnn_w2v = CnnW2v(seed, model_variation,
                     sequence_length, embedding_dim,
                     filter_sizes, num_filters,
                     dropout_prob, hidden_dims, number_samples,
                     num_epochs, val_split,
                     min_word_count, context, weights_file_conv,
                     model_file_conv, paths, None,
                     data_helpers, verbose)
    cnn_w2v.get_data(params[0], params[1], params[2])
    cnn_w2v.build_model()
    print("Convolutional network training")
    history_conv = cnn_w2v.train_model(samples_per_epoch,
                                       labels_conv)
    cnn_w2v.paths[1] = "/var/lib/arhuaco/data/dns_malicious.log"
    result = cnn_w2v.test_model(1000,
                                labels_conv,
                                max_length,
                                n_gram)
    # Graphically plot the results
    plot = Plot()
    # Training vs validation
    plot.history2plot([history_conv.history['real_accuracy'],
                       history_conv.history['val_real_accuracy']],
                       ['Training', 'Validation'],
                       "CNN accuracy", "Epoch", "Accuracy",
                       "/var/lib/arhuaco/data/models/net_cnn_accuracy-%s.pdf"\
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='lower right')
    # Trainning vs validation fpr
    plot.history2plot([history_conv.history['false_pos_rate'],
                       history_conv.history['val_false_pos_rate']],
                       ['Training', 'Validation'],
                       "CNN false positive rate", "Epoch",
                       "False positive rate",
                       "/var/lib/arhuaco/data/models/net_cnn_fpr-%s.pdf"\
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='upper right')

if __name__ == "__main__":
   main(sys.argv[1:])
