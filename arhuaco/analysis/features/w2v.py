# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from __future__ import print_function
from gensim.models import word2vec
from os.path import join, exists, split
import os, sys, getopt
import numpy as np
import logging

# this class applies the word 2 vec method on security monitoring data

class W2V:

    def __init__(self):
        self.initial = None

    def train_word2vec_stream(self, sentence_stream, num_epochs, num_features=10,
                              min_word_count=5, context=10):
        model_dir = '/var/lib/arhuaco/data/models'
        model_name = "{:d}features_{:d}minwords_{:d}context"\
                     .format(num_features, min_word_count, context)
        model_name = join(model_dir, model_name)

        if exists(model_name):
            embedding_model = word2vec.Word2Vec.load(model_name)
            logging.info("Loading existing Word2Vec model \'%s\'"
                         % split(model_name)[-1])
        else:
            # Set values for various parameters
            num_workers = 2  # Number of threads to run in parallel
            downsampling = 1e-3  # Downsample setting for frequent words
            # Initialize and train the model
            print('Initializing Word2Vec model...')
            sentences = next(sentence_stream)
            embedding_model = word2vec.Word2Vec(sentences, workers=num_workers,
                                                size=num_features, min_count=min_word_count,
                                                window=context, sample=downsampling)

            for batch in range(num_epochs):
                sentences = next(sentence_stream)
                embedding_model.build_vocab(sentences, keep_raw_vocab=True, update=True)
                embedding_model.train(sentences, total_examples=embedding_model.corpus_count
                                      , epochs=embedding_model.epochs)
                logging.info("Finished epoch: %d" % batch)
                logging.info("Vocabulary length: %d" % len(embedding_model.wv.index2word))
            if not exists(model_dir):
                os.mkdir(model_dir)
            logging.info('Saving Word2Vec model \'%s\'' % split(model_name)[-1])
            embedding_model.save(model_name)
        # add unknown words
        embedding_list = [embedding_model[w] for w in embedding_model.wv.index2word]
        embedding_list.append(np.random.uniform(-0.25, 0.25, embedding_model.vector_size))
        embedding_weights = [np.array(embedding_list)]

        return [embedding_weights, embedding_model.wv.vocab, embedding_model.wv.index2word]

    def load_word2vec_model(self, model_name):
        model_dir = '/var/lib/arhuaco/data/models'
        model_name = join(model_dir, model_name)
        logging.info("Loading w2v mode: %s" % model_name)

        if exists(model_name):
            embedding_model = word2vec.Word2Vec.load(model_name)
            logging.info("Loading existing Word2Vec model \'%s\'" % split(model_name)[-1])
            # add unknown words
            embedding_list = [embedding_model[w] for w in embedding_model.wv.index2word]
            embedding_list.append(np.random.uniform(-0.25, 0.25, embedding_model.vector_size))
            embedding_weights = [np.array(embedding_list)]

            return [embedding_weights, embedding_model.wv.vocab, embedding_model.wv.index2word]
        else:
            return None

    if __name__ == '__main__':
        from data_helpers import DataHelpers
        from w2v import W2V

        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv,"ht:",["type="])
        except getopt.GetoptError:
            print("test_conv_w2v.py -t <type>")
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print("test_conv_w2v.py -t <type>")
                sys.exit()
            elif opt in ("-t", "--type"):
                type = arg
        if type == "syscall":
            # parameters
            max_length = 10
            n_gram = 20
            sequence_length = max_length*n_gram
            batch_size = 100000
            paths = [ "/var/lib/arhuaco/data/normal_clean.csv", "/var/lib/arhuaco/data/malicious_clean.csv"]
            labels = [ 0, 1 ]
            # Load data
            print("Loading data...")
            # Create objects
            data_helpers = DataHelpers( paths, labels, max_length, n_gram, batch_size)
            w2v = W2V()
            sentence_stream = data_helpers.sentence_stream(batch_size)
            w2v.train_word2vec_stream(sentence_stream, num_features=20, min_word_count=4,
                                      context=10, num_epochs=100)
        elif type == "network":
            # parameters
            max_length = 5
            n_gram = 1
            sequence_length = max_length*n_gram
            batch_size = 100
            paths = [ "/var/lib/arhuaco/data/dns_normal.log", "/var/lib/arhuaco/data/dns_malicious.log"]
            labels = [ 0, 1 ]
            # Load data
            print("Loading data...")
            # Create objects
            data_helpers = DataHelpers( paths, labels, max_length, n_gram, batch_size)
            w2v = W2V()
            sentence_stream = data_helpers.sentence_stream(batch_size)
            w2v.train_word2vec_stream(sentence_stream, num_features=5, min_word_count=1,
                                          context=4, num_epochs=25)
