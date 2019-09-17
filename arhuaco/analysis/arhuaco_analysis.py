import os
import sys, getopt
import numpy as np
import time
import logging

from arhuaco.analysis.features.data_helpers\
     import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.convolutional.cnn_w2v\
     import CnnW2v
from arhuaco.graphics.plot import Plot
from arhuaco.config.configuration import Configuration

from threading import Thread, Event
from queue import Queue, Empty

class ArhuacoAnalysis:

    def __init__(self, input_queue_dict, output_queue):
        self.configuration    = None
        self.input_queue_dict = input_queue_dict
        self.output_queue     = output_queue

    def start_analysis(self):
        # docker_thread = Thread(target=worker)
        syscall_thread = Thread(target=self.do_analyze,kwargs=dict(type="syscall"))
        network_thread = Thread(target=self.do_analyze,kwargs=dict(type="network"))
        # docker_thread.start()
        syscall_thread.start()
        network_thread.start()

    def build_model(self,type="syscall"):
       # Load configuration
        config_object = Configuration()
        if type == "syscall":
            # Load configuration
            config_object.load_configuration("host")
            configuration = config_object.default_config
            configuration['input_queue'] = self.input_queue_dict["syscall_sensor"]

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 100000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file_conv'] = "/var/lib/arhuaco/data/models/sys_W_conv.bin"
            configuration['model_file_conv'] = "/var/lib/arhuaco/data/models/sys_model_conv.json"
        elif type == "network":
            # Load configuration
            config_object = Configuration()
            config_object.load_configuration("network")
            configuration = config_object.default_config
            configuration['input_queue'] = self.input_queue_dict["network_sensor"]

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 10000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file_conv'] = "/var/lib/arhuaco/data/models/net_W_conv.bin"
            configuration['model_file_conv'] = "/var/lib/arhuaco/data/models/net_model_conv.json"

        w2v_model_name = "{:d}features_{:d}minwords_{:d}context".format(
                      configuration['num_features'],
                      configuration['min_word_count'],
                      configuration['context'])

        # Create objects
        # Apply the word2vec processing
        w2v = W2V()
        params = w2v.load_word2vec_model(w2v_model_name)
        embedding_weights=params[0]
        configuration['vocabulary']=params[1]
        configuration['vocabulary_index']=params[2]

        # Create the Convolutional network object
        cnn_w2v = CnnW2v(seed=configuration['seed'],
                  samples_per_batch=configuration['samples_per_batch'],
                  min_word_count=configuration['min_word_count'],
                  context=configuration['context'],
                  weights_file=configuration['weights_file_conv'],
                  model_file=configuration['model_file_conv'],
                  labels=None,
                  verbose=configuration['verbose'])
        cnn_w2v.set_w2v_params(embedding_weights=embedding_weights,
                               vocabulary=configuration['vocabulary'],
                               vocabulary_index=configuration['vocabulary_index'])
        # Buid the model
        # Do I really need to build the model again?
        # What is in the the model.json file then?
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
        cnn_w2v.load_model_weights(configuration['weights_file_conv'])
        return cnn_w2v, configuration

    def do_analyze(self, type=None):
        # Create objects
        model, configuration = self.build_model(type=type)
        # First create the sources of data
        data_helpers = DataHelpers(data_source=configuration['paths'],
                                   label=None,
                                   tokens_per_line=configuration['tokens_per_line'],
                                   number_lines=configuration['number_lines'],
                                   samples_per_batch=configuration['samples_per_batch'],
                                   seed=configuration['seed'])
        # Get the data sources
        online_generator = data_helpers.get_data_stream(configuration['vocabulary'],
                                                        configuration['input_queue'])
        logging.info("Convolutional intrusion detection: %s" % type)
        result = model.analyze_stream(online_generator,self.output_queue)
