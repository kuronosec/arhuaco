from keras.models import Sequential,\
     Model, model_from_json
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import numpy as np

class Plot:

    def load_model(self, path_model, path_weights):
        # load json and create model
        json_file = open(path_model, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(path_weights)
        print("Loaded model from disk")

        return loaded_model

    def model2graph(self, model, path_model, path_weights):
        model = self.load_model("/home/data/models/model.json",
                           "/home/data/models/weights_file_network")
        plot_model(model, to_file='/home/data/models/model_network.png')

    def history2plot(self, history, legend, title,
                     x_label, y_label, path, location,
                     x_lim, y_lim):
        # summarize history
        fig = plt.figure()
        colors = [ "blue", "green", "red", "black"]
        markers = [ "o", "s", "D", "x"]
        linestyles = [ ":", "--", "-."]
        index = 0
        x = np.arange(1,x_lim[1])
        for sequence in history:
            plt.plot(x,
                     sequence,
                     color=colors[index],
                     marker=markers[index],
                     markersize=5,
                     linestyle='None')
            index = index + 1
        plt.grid()
        plt.title(title)
        plt.xticks(x)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.legend( legend, loc=location)
        plt.xlim(x_lim[0], x_lim[1])
        plt.ylim(y_lim[0], y_lim[1])
        if path is not None:
            fig.savefig(path)
            plt.close(fig)
        else:
            plt.show()

    def history2error(self, history, history_error, legend, title,
                     x_label, y_label, path, location,
                     x_lim, y_lim):
        # summarize history
        fig = plt.figure()
        colors = [ "blue", "green", "red"]
        markers = [ "o", "s", "D"]
        linestyles = [ ":", "--", "-."]
        index = 0
        x = np.arange(1,x_lim[1])
        for y in history:
            plt.errorbar(x,
                     y,
                     history_error[index],
                     color=colors[index],
                     marker=markers[index],
                     markersize=5,
                     linestyle='None')
            index = index + 1
        plt.grid()
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.legend( legend, loc=location)
        plt.xlim(x_lim[0], x_lim[1])
        plt.ylim(y_lim[0], y_lim[1])
        if path is not None:
            fig.savefig(path)
            plt.close(fig)
        else:
            plt.show()

