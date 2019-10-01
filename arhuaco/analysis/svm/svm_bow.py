# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from __future__ import print_function

import os

import numpy as np
from arhuaco.analysis.features.data_helpers import DataHelpers

from arhuaco.analysis.util.metric import Metric
from keras.models import Sequential, Model, model_from_json
from keras.layers import Activation, Dense, Dropout,\
                         Embedding, Flatten, Input,\
                         Merge, MaxPooling1D,\
                         Permute
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD
from keras.regularizers import l2

# Support Vector Machine with bag-of-words training for comparison
# with the convolutional neural networks.

class SVM:

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

    def set_bow_params(self,
                       embedding_weights,
                       vocabulary,
                       vocabulary_index):
        # Model parameters
        print("Loading data...")
        self.embedding_weights = embedding_weights
        self.vocabulary = vocabulary
        self.vocabulary_index = vocabulary_index
        print("Vocabulary Size: {:d}".format(
              len(self.vocabulary)))

    def build_model(self,
                    learn_rate=0.001,
                    momentum=0.0,
                    decay=0.0,
                    nesterov=True,
                    regularizer_param=0.01,
                    sequence_length=7,
                    dropout_rate=0.0,
                    embedding_dim=10,
                    ):
        # Building model
        # main sequential model
        self.model = Sequential()
        # self.model.add(Dense(units=len(self.vocabulary),
        #      kernel_regularizer=l2(regularizer_param),
        #      input_dim=len(self.vocabulary)))
        # self.model.add(Activation('sigmoid'))
        self.model.add(Dense(units=1,
              input_dim=len(self.vocabulary),
              kernel_regularizer=l2(regularizer_param)))
        # self.model.add(BatchNormalization())
        self.model.add(Activation('linear'))
        self.model.compile(loss='hinge', optimizer='adadelta',
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
            print("Model loaded from disk.")
        else:
            print("No model found!")

    def train_model(self, training_source, validation_source,
                    samples_per_epoch, number_epochs, val_split):

        if os.path.exists(self.weights_file):
            self.model.load_weights(self.weights_file)
            print("Model loaded from disk.")
        # actually train the model
        history = self.model.fit_generator(verbose=self.verbose,
                             generator=training_source,
                             validation_data=validation_source,
                             steps_per_epoch=samples_per_epoch,
                             epochs=number_epochs,
                             validation_steps=samples_per_epoch\
                             *val_split)
        # Save model
        print("dumping weights to file...")
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

        print("Test model loss: %s"                % result[0])
        print("Test model real accuracy: %s"       % result[1])
        print("Test model false positive rate: %s" % result[2])
        print("Test model real accuracy: %s"       % result[3])
        print("Test model real sensitivity: %s"    % result[4])
        print("Test model real specificity: %s"    % result[5])

        return result

    def analyze_stream(self, data_source,
                       max_length, n_gram,
                       output_queue):
        self.output_queue = output_queue
        data_helpers = DataHelpers( data_source,
                                    None,
                                    max_length,
                                    n_gram,
                                    samples_per_batch=None,
                                    seed=20)
        data_generator = data_helpers.get_data_stream(self.vocabulary,
                                                      data_source)
        while True:
            data = next(data_generator)
            result = self.model.predict(data)
            self.output_queue.put(result)
