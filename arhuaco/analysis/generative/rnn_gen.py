# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from arhuaco.analysis.features.data_helpers\
     import DataHelpers
from tqdm import tqdm
import numpy as np
import random
import sys
import string
import os

# This is the main class for RNN based generative models,
# That creates synthetic data based on previous examples.

class RnnGen:

    def __init__(self, data_helpers, maxlen,
                 step, num_epochs, num_chars,
                 samples_per_epoch, weights_file,
                 model_file, generated_file
                 , number_generated):
        # Parameters
        self.maxlen = maxlen
        self.step = step
        self.num_epochs = num_epochs
        self.num_chars = 0
        self.model = None
        self.data_helpers = data_helpers
        self.data_generator = None
        self.char_indices = None
        self.indices_char = None
        self.samples_per_epoch = samples_per_epoch
        self.weights_file = weights_file
        self.model_file = model_file
        self.generated_file = generated_file
        self.number_generated = number_generated

    def get_data(self):
        self.data_generator = self.data_helpers.generator_from_file(
                              self.data_helpers.data_source[1],
                              self.data_helpers.number_samples)
        # Initialize character set
        chars = sorted(list(set(string.printable+"\n")))
        print('total chars:', len(chars))
        self.num_chars = len(chars)
        self.char_indices = dict((c, i) for i, c in enumerate(chars))
        self.indices_char = dict((i, c) for i, c in enumerate(chars))

    def format_text(self, text):
        # cut the text in semi-redundant
        # sequences of maxlen characters
        sentences = []
        next_chars = []
        for i in range(0, len(text) - self.maxlen, self.step):
            sentences.append(text[i: i + self.maxlen])
            next_chars.append(text[i + self.maxlen])
        print('nb sequences:', len(sentences))
        print('Vectorization...')
        X = np.zeros((len(sentences), self.maxlen,
                    self.num_chars), dtype=np.bool)
        y = np.zeros((len(sentences), self.num_chars),
                    dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                X[i, t, self.char_indices[char]] = 1
            y[i, self.char_indices[next_chars[i]]] = 1

        return (X,y)

    def build_model(self):
        # build the model: a single LSTM
        print('Build model...')
        self.model = Sequential()
        self.model.add(LSTM(128,
                       input_shape=(self.maxlen,
                       self.num_chars)))
        self.model.add(Dense(self.num_chars))
        self.model.add(Activation('softmax'))
        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=optimizer)

    def sample(self, preds, temperature=1.0):
        # helper function to sample an index
        # from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def train_model(self):
        # train the model, output generated text
        # after each iteration
        if os.path.exists(self.weights_file):
            self.model.load_weights(self.weights_file)
            print("Model loaded from disk.")
            x_train = next(self.data_generator)
            text = self.data_helpers.get_text_from_list(
                        x_train)
        else:
            for iteration in range(1):
                x_train = next(self.data_generator)
                text = self.data_helpers.get_text_from_list(
                        x_train)
                print('total chars in text:', len(text))
                X, y = self.format_text(text)
                print('-' * 50)
                print('Iteration', iteration)
                self.model.fit(X, y,
                               batch_size=self.samples_per_epoch,
                               nb_epoch=self.num_epochs)
            # Save model
            print("dumping weights to file...")
            # serialize model to JSON
            model_json = self.model.to_json()
            with open(self.model_file, "w") as json_file:
                json_file.write(model_json)
            self.model.save_weights(self.weights_file,
                                    overwrite=True)
        self.test_model(text)

    def test_model(self, text):
        # Generate new data
        print("Size of text:"+str(len(text)))
        for diversity in [0.2, 0.5, 1.0, 1.2]:
            start_index = random.randint(0, len(text)\
                          - self.maxlen - 1)
            with open(self.generated_file+"-"+str(diversity),
                      "a") as gen_file:
                print()
                print('----- diversity:', diversity)
                # Create a seed for generating data
                generated = ''
                sentence = text[start_index: start_index + self.maxlen]
                generated += sentence
                print('----- Generating with seed: "' + sentence + '"')
                for i in tqdm(range(self.number_generated)):
                    x = np.zeros((1, self.maxlen, self.num_chars))
                    for t, char in enumerate(sentence):
                        x[0, t, self.char_indices[char]] = 1.
                    preds = self.model.predict(x, verbose=0)[0]
                    next_index = self.sample(preds, diversity)
                    next_char = self.indices_char[next_index]
                    generated += next_char
                    sentence = sentence[1:] + next_char
                gen_file.write(generated)
