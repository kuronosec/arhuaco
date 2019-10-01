# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import os

import logging
import numpy as np

from arhuaco.analysis.util.metric import Metric
from arhuaco.analysis.features.data_helpers\
     import DataHelpers
from arhuaco.analysis.features.w2v import W2V

from keras.models import Sequential, Model,\
                         model_from_json
from keras.layers import Activation,\
                         Dense, Dropout, Embedding,\
                         Flatten, Input, Add, Concatenate,\
                         Conv1D, MaxPooling1D
from keras.optimizers import SGD
from keras.regularizers import l2

# Implementation of a classifier for security data anlysis with
# word2vec and convolutional neural networks.

class CnnW2v:

    def __init__(self,
                 seed,
                 samples_per_batch,
                 min_word_count,
                 context,
                 weights_file,
                 model_file,
                 labels,
                 verbose=2):
        # Initialize random values
        np.random.seed(seed)
        # Training parameters
        self.samples_per_batch = samples_per_batch
        # Word2Vec parameters, see train_word2vec
        self.min_word_count = min_word_count
        # Context window size
        self.context = context
        self.weights_file = weights_file
        self.model_file = model_file
        self.embedding_weights = None
        self.vocabulary = None
        self.vocabulary_index = None
        self.model = None
        self.verbose = verbose
        self.output_queue = None
        self.metric = Metric()

    # set the parameters for the word2vec algorithm
    def set_w2v_params(self,
                       embedding_weights,
                       vocabulary,
                       vocabulary_index):
        # Model parameters
        logging.info("Loading data...")
        self.embedding_weights = embedding_weights
        self.vocabulary = vocabulary
        self.vocabulary_index = vocabulary_index
        logging.info("Vocabulary Size: {:d}".format(
              len(self.vocabulary)))

    def build_model(self,
                    learn_rate=0.001,
                    momentum=0.0,
                    decay=0.0,
                    nesterov=True,
                    regularizer_param=0.01,
                    hidden_neurons=20,
                    num_filters=10,
                    filter_sizes=(3, 4, 5),
                    dropout_rate=0.0,
                    embedding_dim=10,
                    pool_size=2,
                    sequence_length=7
                    ):
        ''' This is where the CNN model is built
            Building model
            graph subnet with one input and one output,
            convolutional layers concateneted in parallel '''
        graph_in = Input(shape=(sequence_length,embedding_dim))
        convs = []
        for fsz in filter_sizes:
            # Keep this reference for the time being to
            # update the keras API
            conv = Conv1D(activity_regularizer=l2(
                                   regularizer_param),
                          padding="valid",
                          strides=1,
                          kernel_regularizer=l2(
                                   regularizer_param),
                          filters=num_filters,
                          activation="relu",
                          kernel_size=fsz)(graph_in)
            pool = MaxPooling1D(pool_size=pool_size)(conv)
            flatten = Flatten()(pool)
            convs.append(flatten)

        out = None
        if len(filter_sizes) > 1:
            out = Concatenate()(convs)
        else:
            out = convs[0]

        graph = Model(outputs=out, inputs=graph_in)

        self.model = Sequential()
        self.model.add(Embedding(len(self.vocabulary)+1,
                       embedding_dim,
                       input_length=sequence_length,
                       weights=self.embedding_weights))
        if dropout_rate > 0.0:
           self.model.add(Dropout(dropout_rate,
                           input_shape=(sequence_length,
                           embedding_dim)))
        self.model.add(graph)
        self.model.add(Dense(hidden_neurons))
        if dropout_rate > 0.0:
            self.model.add(Dropout(dropout_rate))
        self.model.add(Activation('relu'))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
        opt = SGD(lr=learn_rate, momentum=momentum,
                  decay=decay, nesterov=nesterov)
        self.model.compile(loss='binary_crossentropy', optimizer=opt,
                           metrics=['accuracy',
                           self.metric.false_pos_rate,
                           self.metric.real_accuracy,
                           self.metric.sensitivity,
                           self.metric.specificity])
        return self.model

    def load_model_weights(self, weights_file):
        # Load the model weight from disk
        if os.path.exists(self.weights_file):
            self.model.load_weights(self.weights_file)
            logging.info("Model loaded from disk.")
        else:
            logging.info("No model found!")

    def train_model(self, training_source, validation_source,
                    samples_per_epoch, number_epochs, val_split):

        if os.path.exists(self.weights_file):
            self.model.load_weights(self.weights_file)
            logging.info("Model loaded from disk.")
        # actually train the model
        history = self.model.fit_generator(verbose=self.verbose,
                             generator=training_source,
                             validation_data=validation_source,
                             steps_per_epoch=samples_per_epoch,
                             epochs=number_epochs,
                             validation_steps=samples_per_epoch\
                             *val_split)
        # Save model
        logging.info("dumping weights to file...")
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(self.model_file, "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights(self.weights_file, overwrite=True)
        return history

    def test_model(self, test_data_source, samples_to_test):
        result = self.model.evaluate_generator(
                                     test_data_source,
                                     steps=samples_to_test)

        logging.info("Test model loss: %s"                % result[0])
        logging.info("Test model real accuracy: %s"       % result[1])
        logging.info("Test model false positive rate: %s" % result[2])
        logging.info("Test model real accuracy: %s"       % result[3])
        logging.info("Test model real sensitivity: %s"    % result[4])
        logging.info("Test model real specificity: %s"    % result[5])

        return result

    def analyze_stream(self, data_source,
                       output_queue):
        self.output_queue = output_queue
        while True:
            original_data, id, data = next(data_source)
            result = {"id":" ","value":None,"payload":None}
            result["id"] = id
            result["value"] = self.model.predict(data)
            result["payload"] = data
            result["original"] = original_data
            self.output_queue.put(result)
