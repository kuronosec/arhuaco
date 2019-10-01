# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

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
from arhuaco.config.configuration import Configuration

class TrainCnnW2v:

    def __init__(self):
        self.configuration = None

    def train(self,
              type="syscall"
              ):
        # Load configuration
        config_object = Configuration()
        if type == "syscall":
            config_object.load_configuration("host")
            configuration = config_object.default_config

            # Training parameters
            configuration['verbose'] = 1
            configuration['samples_per_batch'] = 5
            # Thesis configuration
            configuration['samples_per_epoch'] = 100000
            # Test configuration to show concept
            # configuration['samples_per_epoch'] = 1000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file_conv'] = "/var/lib/arhuaco/data/models/sys_W_conv-%s"\
                                                 % time.strftime("%Y%m%d-%H%M%S")
            configuration['model_file_conv'] = "/var/lib/arhuaco/data/models/sys_model_conv-%s.json"\
                                               % time.strftime("%Y%m%d-%H%M%S")
            # Training dataset
            configuration['paths'] = [ "/var/lib/arhuaco/data/normal_clean_filtered.csv",
                                       "/var/lib/arhuaco/data/malicious_clean_filtered.csv"]

            configuration['pdf_paths'] = ["/var/lib/arhuaco/data/models/sys_cnn_accuracy-%s.pdf"
                                          % time.strftime("%Y%m%d-%H%M%S"),
                                          "/var/lib/arhuaco/data/models/sys_cnn_fpr-%s.pdf"\
                                          % time.strftime("%Y%m%d-%H%M%S")]

        elif type == "network":
            # Load configuration
            config_object = Configuration()
            config_object.load_configuration("network")
            configuration = config_object.default_config

            # Training parameters
            configuration['verbose'] = 1
            configuration['samples_per_batch'] = 5
            # Thesis configuration
            # configuration['samples_per_epoch'] = 10000
            # Test configuration to show concept
            configuration['samples_per_epoch'] = 1000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file_conv'] = "/var/lib/arhuaco/data/models/net_W_conv-%s"\
                                                 % time.strftime("%Y%m%d-%H%M%S")
            configuration['model_file_conv'] = "/var/lib/arhuaco/data/models/net_model_conv-%s.json"\
                                                % time.strftime("%Y%m%d-%H%M%S")
            # Training dataset
            paths = [ "/var/lib/arhuaco/data/dns_normal.log",
                      "/var/lib/arhuaco/data/dns_malicious.log"]

            configuration['pdf_paths'] = ["/var/lib/arhuaco/data/models/net_cnn_accuracy-%s.pdf"
                                          % time.strftime("%Y%m%d-%H%M%S"),
                                          "/var/lib/arhuaco/data/models/net_cnn_fpr-%s.pdf"\
                                          % time.strftime("%Y%m%d-%H%M%S")]

        # Create objects
        # First create the sources of data
        data_helpers = DataHelpers(data_source=configuration['paths'],
                                   label=None,
                                   tokens_per_line=configuration['tokens_per_line'],
                                   number_lines=configuration['number_lines'],
                                   samples_per_batch=configuration['samples_per_batch'],
                                   seed=configuration['seed'])

        # Apply the word2vec processing
        w2v = W2V()
        sentence_stream = data_helpers.sentence_stream(
                                       configuration['samples_per_epoch'])
        params = w2v.train_word2vec_stream(sentence_stream,
                                    num_features=configuration['embedding_dim'],
                                    min_word_count=configuration['min_word_count'],
                                    context=configuration['context'],
                                    num_epochs=configuration['num_epochs'])
        embedding_weights=params[0]
        vocabulary=params[1]
        vocabulary_index=params[2]

        # Create the Convolutional network object
        cnn_w2v = CnnW2v(seed=configuration['seed'],
                  samples_per_batch=configuration['samples_per_batch'],
                  min_word_count=configuration['min_word_count'],
                  context=configuration['context'],
                  weights_file=configuration['weights_file_conv'],
                  model_file=configuration['model_file_conv'],
                  labels=None,
                  verbose=configuration['verbose'])
        cnn_w2v.set_w2v_params(embedding_weights=params[0],
                               vocabulary=params[1],
                               vocabulary_index=params[2])

        # Buid the model
        cnn_w2v.build_model(learn_rate=configuration['learn_rate'],
                            momentum=configuration['momentum'],
                            decay=configuration['decay'],
                            nesterov=configuration['nesterov'],
                            regularizer_param=configuration['regularizer_param'],
                            hidden_neurons=configuration['hidden_dims'],
                            num_filters=configuration['num_filters'],
                            filter_sizes=configuration['filter_sizes'],
                            dropout_rate=configuration['dropout_prob'],
                            embedding_dim=configuration['embedding_dim'],
                            pool_size=configuration['pool_size'],
                            sequence_length=configuration['sequence_length']
                           )
        print("Convolutional training")
        # Get the data sources
        training_generator = data_helpers.get_data_chunk(vocabulary,
                                                   configuration['labels_conv'])
        validation_generator = data_helpers.get_data_chunk(vocabulary,
                                                configuration['labels_conv'])
        test_generator = data_helpers.get_data_chunk(vocabulary,
                                               configuration['labels_conv'])

        # Train and validate the model
        history_object = cnn_w2v.train_model(training_source=training_generator,
                                             validation_source=validation_generator,
                                             samples_per_epoch\
                                             =configuration['samples_per_epoch'],
                                             number_epochs=configuration['num_epochs'],
                                             val_split=configuration['val_split'])
        # Test the model with new data
        result = cnn_w2v.test_model(test_data_source=test_generator,
                                    samples_to_test=configuration['samples_per_epoch'])
        # Graphically plot the results (skip for the time being)
        ''' plot = Plot()
        # Training vs validation
        plot.history2plot([history_object.history['real_accuracy'],
                           history_object.history['val_real_accuracy']],
                           ['Training', 'Validation'],
                           "CNN accuracy", "Epoch", "Accuracy",
                           configuration['pdf_paths'][0],
                           location='lower right')
        # Trainning vs validation fpr
        plot.history2plot([history_object.history['false_pos_rate'],
                           history_object.history['val_false_pos_rate']],
                           ['Training', 'Validation'],
                           "CNN false positive rate", "Epoch",
                           "False positive rate",
                           configuration['pdf_paths'][1],
                           location='upper right') '''

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
       type = ""
    except getopt.GetoptError:
       print("Usage: test_conv_w2v.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("Usage: test_conv_w2v.py -t <type>")
          sys.exit()
       elif opt in ("-t", "--type"):
          type = arg

    # Start the real processing here
    from arhuaco.training.train_cnn_w2v import TrainCnnW2v
    training = TrainCnnW2v()
    if type == "syscall":
        training.train("syscall")
    elif type == "network":
        training.train("network")
    else:
        print("Usage train_cnn_w2v.py -t <type>")

if __name__ == "__main__":
   main(sys.argv[1:])
