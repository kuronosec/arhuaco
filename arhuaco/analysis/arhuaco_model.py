# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

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
from keras import backend as K
from keras.models import model_from_json

import tensorflow as tf

# This is the main class for data analysis in Arhuaco

class ArhuacoModel:

    def __init__(self, input_queue_dict, output_queue):
        self.configuration    = None
        self.input_queue_dict = input_queue_dict
        self.output_queue     = output_queue
        self.abstract_model   = None
        self.data_helper      = None

    def load_configuration(self, type="syscall"):
        config_object = Configuration()
        if type == "syscall":
            config_object.load_configuration("host")
            configuration = config_object.default_config
            if self.input_queue_dict is not None:
                configuration['input_queue'] = self.input_queue_dict["syscall_sensor"]

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 100000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file'] = "/var/lib/arhuaco/data/models/sys_W_conv.bin"
            configuration['model_file'] = "/var/lib/arhuaco/data/models/sys_model_conv.json"
        elif type == "network":
            config_object = Configuration()
            config_object.load_configuration("network")
            configuration = config_object.default_config
            if self.input_queue_dict is not None:
                configuration['input_queue'] = self.input_queue_dict["network_sensor"]

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 10000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file'] = "/var/lib/arhuaco/data/models/net_W_conv.bin"
            configuration['model_file'] = "/var/lib/arhuaco/data/models/net_model_conv.json"
        self.configuration = configuration

    def build_model(self):
        # Create a new Convolutional network object
        cnn_w2v = CnnW2v(seed=self.configuration['seed'],
                  samples_per_batch=self.configuration['samples_per_batch'],
                  min_word_count=self.configuration['min_word_count'],
                  context=self.configuration['context'],
                  weights_file=self.configuration['weights_file'],
                  model_file=self.configuration['model_file'],
                  labels=None,
                  verbose=self.configuration['verbose'])
        cnn_w2v.set_w2v_params(embedding_weights=embedding_weights,
                               vocabulary=self.configuration['vocabulary'],
                               vocabulary_index=self.configuration['vocabulary_index'])
        # Buid the model
        # Do I really need to build the model again?
        # What is in the the model.json file then?
        cnn_w2v.build_model(learn_rate=self.configuration['learn_rate'],
                            momentum=self.configuration['momentum'],
                            decay=self.configuration['decay'],
                            nesterov=self.configuration['nesterov'],
                            regularizer_param=self.configuration['regularizer_param'],
                            hidden_neurons=self.configuration['hidden_dims'],
                            num_filters=self.configuration['num_filters'],
                            filter_sizes=self.configuration['filter_sizes'],
                            dropout_rate=self.configuration['dropout_prob'],
                            embedding_dim=self.configuration['embedding_dim'],
                            pool_size=self.configuration['pool_size'],
                            sequence_length=self.configuration['sequence_length']
                           )
        cnn_w2v.load_model_weights(self.configuration['weights_file'])
        return cnn_w2v

    def load_feature_extractor(self):
        w2v_model_name = "{:d}features_{:d}minwords_{:d}context".format(
                      self.configuration['num_features'],
                      self.configuration['min_word_count'],
                      self.configuration['context'])

        # Apply the word2vec processing
        w2v = W2V()
        params = w2v.load_word2vec_model(w2v_model_name)
        embedding_weights=params[0]
        self.configuration['vocabulary']=params[1]
        self.configuration['vocabulary_index']=params[2]

    def load_model_from_file(self):
        json_file = open(self.configuration['model_file'], 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(self.configuration['weights_file'])
        logging.info("Loaded model from disk")
        self.abstract_model = loaded_model

    def stream_analysis(self, type=None):
        # Create objects
        if K.backend() == "tensorflow":
            with tf.Session(graph = tf.Graph()) as sess:
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
        else:
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

    def initialize_model(self, type=None):
        # Create objects
        self.load_configuration(type=type)
        self.load_feature_extractor()
        self.load_model_from_file()
        # First create the sources of data
        self.data_helper = DataHelpers(data_source=self.configuration['paths'],
                           label=None,
                           tokens_per_line=self.configuration['tokens_per_line'],
                           number_lines=self.configuration['number_lines'],
                           samples_per_batch=self.configuration['samples_per_batch'],
                           seed=self.configuration['seed'])
        self.abstract_model.model._make_predict_function()
        logging.info("Convolutional intrusion detection: %s" % type)

    def predict(self, data):
        input = self.data_helper.string_to_input(
                     self.configuration["vocabulary"],data)
        logging.info(input)
        return self.abstract_model.model.predict(input)
