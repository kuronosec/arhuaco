from sklearn.linear_model import SGDClassifier
import pyprind
from sklearn import metrics
import numpy as np
import time

from arhuaco.analysis.features.data_helpers \
     import DataHelpers
from arhuaco.analysis.features.w2v import W2V
from arhuaco.analysis.svm.svm_w2v import SVM
from arhuaco.graphics.plot import Plot
from arhuaco.config.configuration import Configuration

import sys, getopt

class TrainSvmW2V:

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
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 100000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file_svm'] = "/var/lib/arhuaco/data/models/sys_W_svm-%s"\
                                                 % time.strftime("%Y%m%d-%H%M%S")
            configuration['model_file_svm'] = "/var/lib/arhuaco/data/models/sys_model_svm-%s.json"\
                                               % time.strftime("%Y%m%d-%H%M%S")
            # Training dataset
            configuration['paths'] = [ "/var/lib/arhuaco/data/normal_clean_filtered.csv",
                                       "/var/lib/arhuaco/data/malicious_clean_filtered.csv"]

            configuration['pdf_paths'] = ["/var/lib/arhuaco/data/models/sys_svm_accuracy-%s.pdf"
                                          % time.strftime("%Y%m%d-%H%M%S"),
                                          "/var/lib/arhuaco/data/models/sys_svm_fpr-%s.pdf"\
                                          % time.strftime("%Y%m%d-%H%M%S")]

        elif type == "network":
            # Load configuration
            config_object = Configuration()
            config_object.load_configuration("network")
            configuration = config_object.default_config

            # Training parameters
            configuration['verbose'] = 2
            configuration['samples_per_batch'] = 5
            configuration['samples_per_epoch'] = 1000
            configuration['num_epochs'] = 10
            configuration['val_split'] = 0.1

            configuration['weights_file_svm'] = "/var/lib/arhuaco/data/models/net_W_svm-%s"\
                                                 % time.strftime("%Y%m%d-%H%M%S")
            configuration['model_file_svm'] = "/var/lib/arhuaco/data/models/net_model_svm-%s.json"\
                                                % time.strftime("%Y%m%d-%H%M%S")
            # Training dataset
            configuration['paths'] = [ "/var/lib/arhuaco/data/dns_normal.log",
                                       "/var/lib/arhuaco/data/dns_malicious.log"]
                                     # "/var/lib/arhuaco/data/dns_malicious_generated.log"]

            configuration['pdf_paths'] = ["/var/lib/arhuaco/data/models/net_svm_accuracy-%s.pdf"
                                          % time.strftime("%Y%m%d-%H%M%S"),
                                          "/var/lib/arhuaco/data/models/net_svm_fpr-%s.pdf"\
                                          % time.strftime("%Y%m%d-%H%M%S")]

        # Create objects
        # First create the sources of data
        data_helper = DataHelpers(data_source=configuration['paths'],
                                   label=None,
                                   tokens_per_line=configuration['tokens_per_line'],
                                   number_lines=configuration['number_lines'],
                                   samples_per_batch=configuration['samples_per_batch'],
                                   seed=configuration['seed'])

        # Apply the word2vec processing
        w2v = W2V()
        sentence_stream = data_helper.sentence_stream(
                                      configuration['samples_per_epoch'])
        params = w2v.train_word2vec_stream(sentence_stream,
                                    num_features=configuration['embedding_dim'],
                                    min_word_count=configuration['min_word_count'],
                                    context=configuration['context'],
                                    num_epochs=configuration['num_epochs'])
        embedding_weights=params[0]
        vocabulary=params[1]
        vocabulary_index=params[2]

        # Create the svm network object
        svm_w2v = SVM(seed=configuration['seed'],
                      samples_per_batch=configuration['samples_per_batch'],
                      min_word_count=configuration['min_word_count'],
                      context=configuration['context'],
                      weights_file=configuration['weights_file_svm'],
                      model_file=configuration['model_file_svm'],
                      labels=None,
                      verbose=configuration['verbose'])
        svm_w2v.set_w2v_params(embedding_weights=params[0],
                               vocabulary=params[1],
                               vocabulary_index=params[2])

        # Buid the model
        svm_w2v.build_model(learn_rate=configuration['learn_rate'],
                            momentum=configuration['momentum'],
                            decay=configuration['decay'],
                            nesterov=configuration['nesterov'],
                            regularizer_param=configuration['regularizer_param'],
                            dropout_rate=configuration['dropout_prob'],
                            embedding_dim=configuration['embedding_dim'],
                            sequence_length=configuration['sequence_length']
                           )
        print("svm training")
        # Get the data sources
        training_generator = data_helper.get_data_chunk(vocabulary,
                                                   configuration['labels_svm'])
        validation_generator = data_helper.get_data_chunk(vocabulary,
                                                configuration['labels_svm'])

        # Train and validate the model
        history_object = svm_w2v.train_model(training_source=training_generator,
                                             validation_source=validation_generator,
                                             samples_per_epoch\
                                             =configuration['samples_per_epoch'],
                                             number_epochs=configuration['num_epochs'],
                                             val_split=configuration['val_split'])
        # Test the model with new data
        # Create a new data source for validation with generated data
        configuration['paths'][1] = '/var/lib/arhuaco/data/dns_malicious.log'
        configuration['samples_per_epoch'] = 1000

        validation_data_helper = DataHelpers(data_source=configuration['paths'],
                                      label=None,
                                      tokens_per_line=configuration['tokens_per_line'],
                                      number_lines=configuration['number_lines'],
                                      samples_per_batch=configuration['samples_per_batch'],
                                      seed=configuration['seed']+3)

        test_generator = validation_data_helper.get_data_chunk(vocabulary,
                                                configuration['labels_svm'])

        result = svm_w2v.test_model(test_data_source=test_generator,
                                    samples_to_test=configuration['samples_per_epoch'])
        # Graphically plot the results
        plot = Plot()
        # Training vs validation accuracy
        plot.history2plot([history_object.history['real_accuracy'],
                           history_object.history['val_real_accuracy']],
                           ['Training', 'Validation'],
                           "svm accuracy", "Epoch", "Accuracy",
                           configuration['pdf_paths'][0],
                           'lower right',
                           [ 0, 9], [ 0.8, 1.0 ])
        # Trainning vs validation fpr
        plot.history2plot([history_object.history['false_pos_rate'],
                           history_object.history['val_false_pos_rate']],
                           ['Training', 'Validation'],
                           "svm false positive rate", "Epoch",
                           "False positive rate",
                           configuration['pdf_paths'][1],
                           'upper right',
                           [ 0, 9 ], [ 0, 0.2 ])

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:",["type="])
       type = ""
    except getopt.GetoptError:
       print("Usage: test_svm_w2v.py -t <type>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("Usage: test_svm_w2v.py -t <type>")
          sys.exit()
       elif opt in ("-t", "--type"):
          type = arg

    # Start the real processing here
    from arhuaco.training.train_svm_w2v import TrainSvmW2V
    training = TrainSvmW2V()
    if type == "syscall":
        training.train("syscall")
    elif type == "network":
        training.train("network")
    else:
        print("Usage train_svm_w2v.py -t <type>")

if __name__ == "__main__":
   main(sys.argv[1:])
