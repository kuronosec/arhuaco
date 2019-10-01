# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from sklearn.linear_model import SGDClassifier
import pyprind
from sklearn import metrics
import numpy as np

from arhuaco.analysis.features.data_helpers import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.svm.svm_hot import SVM
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
    min_word_count = 5  # Minimum word count
    context = 10  # Context window size
    paths = [ "/var/lib/arhuaco/data/normal_clean.csv", "/var/lib/arhuaco/data/malicious_clean.csv"]
    labels = [ 0, 1 ]
    number_samples = 2
    number_samples_w2v = 10000
    num_epochs = 10
    embedding_dim = 10
    # Model Hyperparameters
    max_length = 7
    n_gram = 6
    # Create objects
    data_helpers = DataHelpers( paths, labels, max_length, n_gram, number_samples)
    w2v = W2V()
    sentence_stream = data_helpers.sentence_stream(number_samples_w2v)
    params = w2v.train_word2vec_stream(sentence_stream,
                              num_features=embedding_dim,
                              min_word_count=min_word_count, context=context,
                              num_epochs=num_epochs)
    # Create the model
    classes = np.array([0, 1])
    clf = SGDClassifier(loss='hinge', penalty="l2",
                        eta0=0.01, learning_rate='constant')
    # Data load
    data_generator = data_helpers.get_data_chunk(params[1])
    # Training the model
    train_accuracy = []
    test_accuracy = []
    x_train, y_train = next(data_generator)
    clf.partial_fit(x_train, y_train, classes=classes)
    for batch in range(num_epochs):
        for sample in range(1000):
            x_train_aux, y_train_aux = next(data_generator)
            # x_test_aux, y_test_aux = next(data_generator)
            x_train = np.concatenate([x_train, x_train_aux], 0)
            y_train = np.concatenate([y_train, y_train_aux], 0)
            # x_test  = np.concatenate([x_test, x_test_aux], 0)
            # y_test  = np.concatenate([y_test, y_test_aux], 0)
        clf.partial_fit(x_train, y_train)
        print("Batch: %d" % batch)
        print('Train Accuracy: %.3f' % clf.score(x_train, y_train))
        # print('Test Accuracy: %.3f' % clf.score(x_test, y_test))
        train_accuracy.append(clf.score(x_train, y_train))
        # test_accuracy.append(clf.score(x_test, y_test))
    # Plot the results
    plot = Plot()
    plot.history2plot([train_accuracy],"Model accuracy", "Epoch", "Accuracy")

def analyze_network():
    clf = SGDClassifier(loss='hinge', penalty="l2")
    # Word2Vec parameters, see train_word2vec
    min_word_count = 1  # Minimum word count
    context = 4  # Context window size
    paths = [ "/var/lib/arhuaco/data/dns_normal.log", "/var/lib/arhuaco/data/dns_malicious.log"]
    labels = [ 0, 1 ]
    number_samples = 10
    num_epochs = 100
    embedding_dim = 5
    # Model Hyperparameters
    max_length = 5
    n_gram = 1

    # Create objects
    data_helpers = data_helpers = DataHelpers( paths, labels, max_length, n_gram, number_samples)
    w2v = W2V()
    # Load data
    print("Loading data...")
    x, y, vocabulary, vocabulary_inv = data_helpers.load_data()
    embedding_weights, vocabulary = w2v.train_word2vec(x, embedding_dim, min_word_count, context)

    classes = np.array([0, 1])
    # Data load
    data_generator = data_helpers.get_data_chunk(vocabulary)
    # Training the model
    train_accuracy = []
    train_loss = []
    test_accuracy = []
    test_loss = []
    for batch in range(num_epochs):
        x_train, y_train = next(data_generator)
        x_test, y_test = next(data_generator)
        clf.partial_fit(x_train, y_train, classes=classes)
        print("Batch: %d" % batch)
        print('Train Accuracy: %.3f' % clf.score(x_train, y_train))
        print('Test Accuracy: %.3f' % clf.score(x_test, y_test))
        train_accuracy.append(clf.score(x_train, y_train))
        test_accuracy.append(clf.score(x_test, y_test))
    # Plot the results
    plot = Plot()
    plot.history2plot([train_accuracy, test_accuracy],
                      "Model accuracy", "Epoch", "Accuracy")

if __name__ == "__main__":
   main(sys.argv[1:])
