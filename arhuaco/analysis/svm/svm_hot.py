from __future__ import print_function

import os
import numpy as np

from arhuaco.analysis.util.metric import Metric
from arhuaco.analysis.features.data_helpers import DataHelpers

from keras.models import Sequential, Model, model_from_json
from keras.layers import Activation, Dense, Dropout,\
                         Embedding, Flatten, Input,\
                         Merge, Convolution1D, MaxPooling1D,\
                         Permute
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD
from keras.regularizers import l2, activity_l2

class SVM:

    def __init__(self, seed, sequence_length, embedding_dim,
                 dropout_prob, hidden_dims, batch_size,
                 num_epochs, val_split, min_word_count,
                 context, action, weights_file,
                 sentence, paths, labels, data_helpers):
        # Initialize random values
        np.random.seed(seed)

        # Parameters
        # Model Hyperparameters
        self.sequence_length = sequence_length
        self.embedding_dim = embedding_dim
        self.dropout_prob = dropout_prob
        self.hidden_dims = hidden_dims
        # Training parameters
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.val_split = val_split
        # Word2Vec parameters, see train_word2vec
        self.min_word_count = min_word_count
        # Context window size
        self.context = context
        self.action = action
        self.weights_file = weights_file
        self.sentence = sentence
        self.embedding_weights = None
        self.vocabulary = None
        self.vocabulary_index = None
        self.model = None
        self.data_helpers = data_helpers
        self.metric = Metric()

    def get_data(self, embedding_weights, vocabulary, vocabulary_index):
        # Model parameters
        print("Loading data...")
        self.embedding_weights = embedding_weights
        self.vocabulary = vocabulary
        self.vocabulary_index = vocabulary_index
        print("Vocabulary Size: {:d}".format(len(self.vocabulary)))

    def build_model(self):
        # Building model
        # main sequential model
        self.model = Sequential()
        self.model.add(Dense(self.hidden_dims,
                       input_dim=len(self.vocabulary),
                             W_regularizer=l2(0.01)))
        self.model.add(Activation('relu'))
        self.model.add(Dense(output_dim=1,
                             W_regularizer=l2(0.01)))
        self.model.add(BatchNormalization())
        self.model.add(Activation('linear'))
        self.model.compile(loss='hinge', optimizer='adadelta',
                   metrics=['accuracy',
                            self.metric.false_pos_rate,
                            self.metric.real_accuracy,
                            self.metric.sensitivity,
                            self.metric.specificity])

    def train_model(self, samples_per_epoch):
        # Training the model
        # data_generator = self.data_helpers.get_data_chunk(self.vocabulary)
        data_generator = self.data_helpers.get_BoW_chunk(self.vocabulary)
        if os.path.exists(self.weights_file):
            self.model.load_weights(self.weights_file)
            print("Loading model from disk.")
        history = self.model.fit_generator(data_generator,
                             samples_per_epoch=samples_per_epoch,
                             nb_epoch=self.num_epochs)
        # Save model
        print("dumping weights to file...")
        # serialize model to JSON
        model_json = self.model.to_json()
        with open("/home/data/models/model.json", "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights(self.weights_file, overwrite=True)
        return history

    def test_model(self, number_samples):
        # Testing the model
        data_generator = self.data_helpers.get_BoW_chunk(self.vocabulary)
        result = self.model.evaluate_generator(
                      data_generator, val_samples=number_samples)
        print("Test model loss: %s" % result[0])
        print("Test model accuracy: %s" % result[1])
        print("Test model recall: %s" % result[2])
        print("Test model precision: %s" % result[3])
        print("Test model false positive rate: %s" %result[4])
        return result
