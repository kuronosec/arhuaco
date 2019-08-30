from __future__ import print_function

import os
import sys, getopt
import numpy as np
import time

from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier

from arhuaco.analysis.features.data_helpers\
     import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.convolutional.cnn_w2v\
     import CnnW2v
from arhuaco.config.configuration import Configuration

class GridSearch:

    def __init__(self):
        self.configuration = None

    def optimize_cnn_hyperparameters(self,
                                     tokens_per_line,
                                     number_lines,
                                     type="syscall"
                                    ):
        # Load configuration
        config_object = Configuration()
        if type == "syscall":
            config_object.load_configuration("host")
            configuration = config_object.default_config

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 10000
            configuration['num_epochs'] = 100
            configuration['val_split'] = 0.1

            configuration['weights_file_conv'] = "/var/lib/arhuaco/data/models/sys_W_conv-%s"\
                                                 % time.strftime("%Y%m%d-%H%M%S")
            configuration['model_file_conv'] = "/var/lib/arhuaco/data/models/sys_model_conv-%s.json"\
                                               % time.strftime("%Y%m%d-%H%M%S")
            # Training dataset
            configuration['paths'] = [ "/var/lib/arhuaco/data/normal_clean_filtered.csv",
                                       "/var/lib/arhuaco/data/malicious_clean_filtered.csv"]
        elif type == "network":
            # Load configuration
            config_object = Configuration()
            config_object.load_configuration("network")
            configuration = config_object.default_config

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 1000
            configuration['num_epochs'] = 100
            configuration['val_split'] = 0.1

            configuration['weights_file_conv'] = "/var/lib/arhuaco/data/models/net_W_conv-%s"\
                                                 % time.strftime("%Y%m%d-%H%M%S")
            configuration['model_file_conv'] = "/var/lib/arhuaco/data/models/net_model_conv-%s.json"\
                                                % time.strftime("%Y%m%d-%H%M%S")
            # Training dataset
            paths = [ "/var/lib/arhuaco/data/dns_normal.log",
                      "/var/lib/arhuaco/data/dns_malicious.log"]

        # Create objects
        # First create the sources of data
        data_helpers = DataHelpers(data_source=configuration['paths'],
                                   label=None,
                                   tokens_per_line=tokens_per_line,
                                   number_lines=number_lines,
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

        print("Convolutional optimization")
        # Get the data sources
        training_generator = data_helpers.get_data_chunk(vocabulary,
                                                   configuration['labels_conv'])
        validation_generator = data_helpers.get_data_chunk(vocabulary,
                                                configuration['labels_conv'])
        test_generator = data_helpers.get_data_chunk(vocabulary,
                                               configuration['labels_conv'])

        # Create model for grid search
        model = KerasClassifier(build_fn=cnn_w2v.build_model, epochs=8,
                                batch_size=10, verbose=3)

        # Define the grid search parameters
        learn_rate = [0.001, 0.01, 0.1]
        momentum = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]
        decay=[0.0, 1e-5, 1e-6, 1e-7]
        nesterov=[True, False]
        regularizer_param=[0.1, 0.01, 0.001]
        hidden_neurons=[5, 10, 20, 30]
        num_filters=[5, 10, 20, 30]
        filter_sizes=[(1,2,3,4),(3, 4, 5),(5,6)]
        dropout_rate=[0.0, 0.5, 0.1, 0.01]
        embedding_dim=[configuration['embedding_dim']]
        pool_size=[2, 3, 4]
        sequence_length=[tokens_per_line*number_lines]

        print("Starting grid search for %d tokens per line and %d lines"
              % (tokens_per_line, number_lines))
        param_grid = dict(learn_rate=learn_rate,
                          momentum=momentum,
                          decay=decay,
                          nesterov=nesterov,
                          regularizer_param=regularizer_param,
                          hidden_neurons=hidden_neurons,
                          num_filters=num_filters,
                          filter_sizes=filter_sizes,
                          dropout_rate=dropout_rate,
                          embedding_dim=embedding_dim,
                          pool_size=pool_size,
                          sequence_length=sequence_length)

        grid = GridSearchCV(estimator=model, param_grid=param_grid,
                            n_jobs=-1, verbose=3)

        print("Extracting data from source...")
        X, Y = next(training_generator)
        # TODO: fix this! It is too slow...
        for i in range(configuration['samples_per_epoch']):
            X_i, Y_i = next(training_generator)
            X = np.append(X, X_i, axis=0)
            Y = np.append(Y, Y_i, axis=0)
        print("Starting grid search trainings...")
        grid_result = grid.fit(X,Y, verbose=3)
        # summarize results
        print("Best: %f using %s" % (grid_result.best_score_,
                                     grid_result.best_params_))
        means = grid_result.cv_results_['mean_test_score']
        stds = grid_result.cv_results_['std_test_score']
        params = grid_result.cv_results_['params']
        for mean, stdev, param in zip(means, stds, params):
            print("%f (%f) with: %r" % (mean, stdev, param))

    def optimize_data_format(self, type="syscall"):
        # Optimize the parameters that define the format
        # of the input object
        tokens_per_line=[4,5,6,7]
        number_lines=[3,6,20,30]
        for i in tokens_per_line:
            for j in number_lines:
                self.optimize_cnn_hyperparameters(i, j, type=type)

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
       type = ""
    except getopt.GetoptError:
       print("Usage: grid_search.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("Usage: grid_search.py -t <type>")
          sys.exit()
       elif opt in ("-t", "--type"):
          type = arg

    # strat the real processing here
    from arhuaco.analysis.optimization.grid_search import GridSearch
    grid_optimization = GridSearch()
    if type == "syscall":
        # grid_optimization.optimize_cnn_hyperparameters("syscall")
        grid_optimization.optimize_data_format("syscall")
    elif type == "network":
        # grid_optimization.optimize_cnn_hyperparameters("network")
        grid_optimization.optimize_data_format("network")
    else:
        print("Usage: grid_search.py -t <type>")

if __name__ == "__main__":
   main(sys.argv[1:])
