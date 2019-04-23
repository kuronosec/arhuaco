from sklearn.linear_model import SGDClassifier
import pyprind
from sklearn import metrics
import numpy as np
import time

from arhuaco.analysis.features.data_helpers import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.svm.svm_bow import SVM
from arhuaco.graphics.plot import Plot

import sys, getopt

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
    except getopt.GetoptError:
       print("test_svm_hot.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("test_svm_hot.py -t <type>")
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
    weights_file_svm = "/home/data/models/sys_W_svm-%s"\
                       % time.strftime("%Y%m%d-%H%M%S")
    model_file_svm = "/home/data/models/sys_model_svm-%s.json"\
                     % time.strftime("%Y%m%d-%H%M%S")
    # Training dataset
    paths = [ "/home/data/normal_clean.csv",
              "/home/data/malicious_clean.csv"]
    # Training labels
    labels_svm  = [ -1, 1 ]

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
    svm = SVM(seed, sequence_length, embedding_dim,
              dropout_prob, hidden_dims, number_samples,
              num_epochs, val_split, min_word_count,
              context, weights_file_svm, model_file_svm,
              paths, None, data_helpers, verbose)
    svm.get_data(params[0], params[1], params[2])
    svm.build_model()
    print("SVM syscall training")
    history_svm = svm.train_model(samples_per_epoch,
                                  labels_svm)
    result = svm.test_model(10000,
                            labels_svm,
                            max_length,
                            n_gram)
    # Graphically plot the results
    plot = Plot()
    # Training vs validation
    plot.history2plot([history_svm.history['real_accuracy'],
                       history_svm.history['val_real_accuracy']],
                       ['Training', 'Validation'],
                       "SVM accuracy", "Epoch", "Accuracy",
                       "/home/data/models/sys_svm_accuracy-%s.pdf"
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='lower right')
    # Trainning vs validation fpr
    plot.history2plot([history_svm.history['false_pos_rate'],
                       history_svm.history['val_false_pos_rate']],
                       ['Training', 'Validation'],
                       "SVM false positive rate", "Epoch",
                       "False positive rate",
                       "/home/data/models/sys_svm_fpr-%s.pdf"\
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='upper right')

def analyze_network():
    # Parameters
    seed = 5
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
    # Number of neurons in the hidden layer
    hidden_dims = 10
    dropout_prob = (0.0, 0.0)

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
    weights_file_svm = "/home/data/models/net_W_svm-%s"\
                       % time.strftime("%Y%m%d-%H%M%S")
    model_file_svm = "/home/data/models/net_model_svm-%s.json"\
                     % time.strftime("%Y%m%d-%H%M%S")
    # Training dataset
    paths = [ "/home/data/dns_normal.log",
              #"/home/data/dns_malicious.log"]
              "/home/data/dns_malicious_generated.log"]
    # Training labels
    labels_svm  = [ -1, 1 ]

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
    svm = SVM(seed, sequence_length, embedding_dim,
              dropout_prob, hidden_dims, number_samples,
              num_epochs, val_split, min_word_count,
              context, weights_file_svm, model_file_svm,
              paths, None, data_helpers, verbose)
    svm.get_data(params[0], params[1], params[2])
    svm.build_model()
    print("SVM network training")
    history_svm = svm.train_model(samples_per_epoch,
                                  labels_svm)
    # svm.paths[1] = "/home/data/dns_malicious.log"
    result = svm.test_model(1000,
                            labels_svm,
                            max_length,
                            n_gram)
    # Graphically plot the results
    plot = Plot()
    # Training vs validation accuracy
    plot.history2plot([history_svm.history['real_accuracy'],
                       history_svm.history['val_real_accuracy']],
                       ['Training', 'Validation'],
                       "SVM accuracy", "Epoch", "Accuracy",
                       "/home/data/models/net_svm_accuracy-%s.pdf"\
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='lower right')
    # Trainning vs validation fpr
    plot.history2plot([history_svm.history['false_pos_rate'],
                       history_svm.history['val_false_pos_rate']],
                       ['Training', 'Validation'],
                       "SVM false positive rate", "Epoch",
                       "False positive rate",
                       "/home/data/models/net_svm_fpr-%s.pdf"\
                       % time.strftime("%Y%m%d-%H%M%S"),
                       location='upper right')

if __name__ == "__main__":
   main(sys.argv[1:])
