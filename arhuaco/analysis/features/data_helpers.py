# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import numpy as np
import re
import itertools
import random
import os
import pandas as pd
import logging

from arhuaco.analysis.features.preprocess_data\
     import PreprocessData
from collections import Counter
from gensim.models import word2vec
from sklearn.feature_extraction.text\
     import CountVectorizer

# This class contains several utilities for processing
# input security monitoring data.

class DataHelpers:

    def __init__(self, data_source, label,
                 tokens_per_line, number_lines,
                 samples_per_batch, seed):
        self.data_source = data_source
        self.label = label
        self.tokens_per_line = tokens_per_line
        self.number_lines = number_lines
        self.samples_per_batch = samples_per_batch
        self.seed = seed
        self.prep_data = PreprocessData()

    def load_data_and_labels(self):
        # Load data from files
        positive_stream = self.generator_from_file(self.data_source[0],
                                                   self.samples_per_batch)
        positive_examples = next(positive_stream)
        negative_stream = self.generator_from_file(self.data_source[1],
                                                   self.samples_per_batch)
        negative_examples = next(negative_stream)
        positive_examples = self.create_ngrams(positive_examples)
        negative_examples = self.create_ngrams(negative_examples)
        positive_labels  = [ self.label[0] for i in range(len(positive_examples))]
        negative_labels = [ self.label[1] for j in range(len(negative_examples))]
        x = positive_examples + negative_examples
        y = np.concatenate([positive_labels, negative_labels], 0)
        return [x, y]

    def build_vocab(self, sentences):
        # Build vocabulary
        word_counts = Counter(itertools.chain(*sentences))
        # Mapping from index to word
        vocabulary_inv = [x[0] for x in word_counts.most_common()]
        # Mapping from word to index
        vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
        return [vocabulary, vocabulary_inv]

    def build_input_data(self, sentences, labels, vocabulary):
        x = np.array([[vocabulary[word].index if word in vocabulary
                     else len(vocabulary)
                     for word in sentence] for sentence in sentences])
        if labels is not None:
           y = np.array(labels)
        else:
           y = None
        return [x, y]

    def load_data(self):
        # Load and preprocess data
        sentences, labels = self.load_data_and_labels()
        sentences_padded = self.pad_sentences(sentences)
        vocabulary, vocabulary_inv = self.build_vocab(sentences_padded)
        # x, y = build_input_data(sentences_padded, labels, vocabulary)
        x = sentences_padded
        y = np.array(labels)
        return [ x, y, None, None]

    def generator_from_file(self, path, samples_per_batch):
        file = open(path,  'r')
        file_size = os.stat(path).st_size
        random.seed(self.seed)
        # Number of samples is the number of batches
        # times the size of each batch
        while True:
            offset = random.randrange(file_size)
            file.seek(offset)
            # TODO: look for a more elegant way!
            stream = self.get_stream(file, chunk_size = samples_per_batch*self.number_lines)
            yield next(stream).values.tolist()

    def get_text_from_list(self, text_list):
        text = ""
        for list in text_list:
            line = ' '.join(list)
            text = text+' '.join(line.split())+"\n"
        return text

    def preprocess_input(self, sentences, in_train=True):
        # Look for a better way to process this:
        # When training sentences is a list of lists
        # In testing sentences is a list of strings
        # So for the moment process them in a different way
        input_text = None
        if in_train:
            # Eliminate white spaces
            input_text = [s[0].strip() for s in sentences]
            # Take only the first part of each sentence
            input_text = [s.split()[:self.tokens_per_line] for s in input_text]
            # Add a padding for short sentences
            input_text = self.pad_sentences(input_text)
            # Concatenate several sentences toguether
            input_text = self.create_ngrams(input_text)
        else:
            # Eliminate white spaces
            input_text = [s.strip() for s in sentences]
            # Take only the first part of each sentence
            input_text = [s.split()[:self.tokens_per_line] for s in input_text]
            # Add a padding for short sentences
            input_text = self.pad_sentences(input_text)
            # Concatenate several sentences toguether
            # This seems quite a ugly hack, look for a better
            # way to do it
            aux_input_text = []
            for list in input_text:
                aux_input_text=aux_input_text+list
            input_text = [aux_input_text]
        return input_text

    def pad_sentences(self, sentences, padding_word="<PAD/>"):
        sequence_length = self.tokens_per_line
        padded_sentences = []
        for i in range(len(sentences)):
            sentence = sentences[i]
            num_padding = sequence_length - len(sentence)
            new_sentence = sentence + [padding_word] * num_padding
            padded_sentences.append(new_sentence)
        return padded_sentences

    def create_ngrams(self, sentences):
        ngram_sentences = []
        i = 0
        while i < len(sentences)-self.number_lines:
            sentence = []
            for j in range(self.number_lines):
                sentence = sentence+sentences[i+j]
            ngram_sentences.append(sentence)
            i = i+self.number_lines
        return ngram_sentences

    def get_file(self, path, chunk_size):
        chunk = next(pd.read_csv(path, header=None, index_col=None,
                                 chunksize=chunk_size))
        return chunk

    def get_stream(self, file, chunk_size):
        stream = pd.read_csv(file, sep='\n', chunksize=chunk_size)
        return stream

    def sentence_stream(self, samples_per_batch):
        # Load data from files
        positive_stream = self.generator_from_file(self.data_source[0],
                                                   samples_per_batch)
        negative_stream = self.generator_from_file(self.data_source[1],
                                                   samples_per_batch)
        while True:
            # Extract the next data samples
            positive_examples = self.preprocess_input(next(positive_stream))
            negative_examples = self.preprocess_input(next(negative_stream))
            # Concatenate samples
            sentences = positive_examples + negative_examples
            yield sentences

    def get_data_chunk(self, vocabulary, label):
        if label is not None:
            self.label = label
        # Load data from files
        gen_pos = self.generator_from_file(self.data_source[0],
                                           self.samples_per_batch)
        gen_neg = self.generator_from_file(self.data_source[1],
                                           self.samples_per_batch)
        while True:
            # Extract the next data samples
            positive_examples = self.preprocess_input(next(gen_pos))
            negative_examples = self.preprocess_input(next(gen_neg))
            # Create the labels
            positive_labels  = [ self.label[0] for i \
                                 in range(len(positive_examples))]
            negative_labels = [ self.label[1] for j \
                                 in range(len(negative_examples))]

            x = positive_examples + negative_examples
            y = np.concatenate([positive_labels, negative_labels], 0)

            x, y = self.build_input_data(x, y, vocabulary)

            # Shuffle data
            shuffle_indices = np.random.permutation(np.arange(len(y)))
            x_shuffled = x[shuffle_indices]
            y_shuffled = y[shuffle_indices]
            yield (x_shuffled, y_shuffled)

    def get_data_BoW_chunk(self, vocabulary_hash, label):
        if label is not None:
            self.label = label
        # Load data from files
        gen_pos = self.generator_from_file(self.data_source[0],
                                           self.samples_per_batch)
        gen_neg = self.generator_from_file(self.data_source[1],
                                           self.samples_per_batch)
        vocabulary = {word: i for i, word in enumerate(vocabulary_hash)}
        count_vect = CountVectorizer(vocabulary=vocabulary)
        while True:
            # Extract the next data samples
            positive_examples = self.preprocess_input(next(gen_pos))
            negative_examples = self.preprocess_input(next(gen_neg))
            # Create the labels
            positive_labels  = [ self.label[0] for i \
                                 in range(len(positive_examples))]
            negative_labels = [ self.label[1] for j \
                                in range(len(negative_examples))]

            x = positive_examples + negative_examples
            y = np.concatenate([positive_labels, negative_labels], 0)

            x_sentences = [ " ".join(list) for list in x]
            x = count_vect.transform(x_sentences).toarray()
            # Shuffle data
            shuffle_indices = np.random.permutation(np.arange(len(y)))
            x_shuffled = x[shuffle_indices]
            y_shuffled = y[shuffle_indices]
            yield (x_shuffled, y_shuffled)

    # Read the real stream of data from the input iterator
    def get_data_stream(self, vocabulary, data_source):
        while True:
            # Extract the next data to be analyzed
            input_data = []
            sample = {}
            sample = data_source.get()
            id = sample["id"]
            next_input = sample["data"]
            original_input = next_input
            for line in next_input:
                # Eliminate bad characters
                input_line = self.prep_data.clean_str(line)
                input_data.append(input_line)
            processed_data = self.preprocess_input(input_data, in_train=False)
            x, y = self.build_input_data(processed_data, None, vocabulary)
            yield original_input, id, x
