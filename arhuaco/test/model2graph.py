# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

from keras.utils import plot_model
from keras.models import Sequential, Model, model_from_json

def load_model(path_model, path_weights):
    # load json and create model
    json_file = open(path_model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(path_weights)
    print("Loaded model from disk")
    return loaded_model

if __name__ == "__main__":
    model = load_model("/var/lib/arhuaco/data/models/model.json",
                       "/var/lib/arhuaco/data/models/weights_file_network")
    plot_model(model, to_file='/var/lib/arhuaco/data/models/model_network.png')
