class Configuration:

    def __init__(self):
        self.configuration = self.analyze_config_file()
        self.defalt_config = None

    def analyze_config_file(self):
        return None

    def load_configuration(self, type):
        if type == "host":
            self.default_config = {
                # Parameters
                # Word2Vec parameters, see train_word2vec
                # Minimum word count
                'min_word_count' : 5,
                # Number of words that make sense in the context
                'context' : 10,
                'num_features':10,
                'seed': 5,
                'model_variation' : 'CNN-non-static',
                'verbose' : 1,
                # Model Hyperparameters
                # Max lenght of one sentence
                'tokens_per_line' : 7,
                # Number of lines included in the
                # series
                'number_lines' : 6,
                # Total lenght of the classification
                # object max_length*n_gram
                'sequence_length' : 7*6,
                # Size of the vector representing each word
                'embedding_dim' : 10,
                # Conv. Filters applied to the text
                'filter_sizes' : (3, 4, 5),
                # Total filters used
                'num_filters' : 20,
                'dropout_prob' : 0.0,
                # Number of neurons in the hidden layer
                'hidden_dims' : 10,
                # Training parameters
                'learn_rate' : 0.001,
                'momentum' : 0.8,
                'decay' : 1e-5,
                'nesterov' : False,
                'regularizer_param' : 0.001,
                'hidden_dims' : 30,
                'num_filters' : 30,
                'filter_sizes' : (1,2,3,4),
                'dropout_prob' : 0.0,
                'pool_size' : 2,
                'number_samples' : 5,
                'samples_per_epoch' : 10000,
                'num_epochs' : 100,
                'val_split' : 0.1,
                'weights_file_conv' : "/var/lib/arhuaco/data/models/sys_W_conv",
                'model_file_conv' : "/var/lib/arhuaco/data/models/sys_model_conv.json",
                # Training dataset
                'paths' : [ "/var/lib/arhuaco/data/normal_clean.csv",
                          "/var/lib/arhuaco/data/malicious_clean.csv"],
                # Training labels
                'labels_conv' : [ 0, 1 ],
                'labels_svm' : [-1,1]
            }
        elif type == "network":
            self.default_config = {
                # Parameters
                # Word2Vec parameters, see train_word2vec
                # Minimum word count
                'min_word_count' : 1,
                # Number of words that make sense in the context
                'context' : 4,
                'num_features':10,
                'seed' : 5,
                'model_variation' : 'CNN-non-static',
                # Model Hyperparameters
                # Max lenght of one sentence
                'tokens_per_line' : 5,
                # Number of lines included in the
                # series
                'number_lines' : 1,
                # Total lenght of the classification
                # object
                'sequence_length' : 5*1,
                # Size of the vector representing each word
                'embedding_dim' : 10,
                # Conv. Filters applied to the text
                'filter_sizes' : (2, 3),
                # Total filters used
                'num_filters' : 3,
                'dropout_prob' : 0.0,
                # Number of neurons in the hidden layer
                'hidden_dims' : 10,
                # Training parameters
                'learn_rate' : 0.01,
                'momentum' : 0.9,
                'decay' : 1e-5,
                'nesterov' : True,
                'regularizer_param' : 0.001,
                'hidden_dims' : 20,
                'num_filters' : 10,
                'filter_sizes' : (2,3),
                'dropout_prob' : 0.0,
                'pool_size' : 2,
                'number_samples' : 5,
                'samples_per_epoch' : 1000,
                'num_epochs' : 100,
                'val_split' : 0.1,
                'verbose' : 1,
                'weights_file_conv' : "/var/lib/arhuaco/data/models/net_W_conv",
                'model_file_conv' : "/var/lib/arhuaco/data/models/net_model_conv.json",
                # Training dataset
                'paths' : [ "/var/lib/arhuaco/data/dns_normal.log",
                            "/var/lib/arhuaco/data/dns_malicious.log"],
                # Training labels
                'labels_conv' : [ 0, 1 ],
                'labels_svm' : [-1,1]
           }
