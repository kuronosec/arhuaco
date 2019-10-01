# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import os

import numpy as np
import keras.backend as K

# A set of utilities for calculating evaluation metrics.

class Metric:

    # TODO: is there a way to make a more compact method
    # that calculates all theses metrics?
    def false_pos_rate(self, y_true, y_pred):
        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.round(K.clip(y_true, 0, 1))
        y_neg = 1 - y_pos
        tn = K.sum(y_neg * y_pred_neg)
        fp = K.sum(y_neg * y_pred_pos)
        false_positive_rate = fp/(fp+tn)

        return false_positive_rate

    def real_accuracy(self, y_true, y_pred):
        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.round(K.clip(y_true, 0, 1))
        y_neg = 1 - y_pos
        tp = K.sum(y_pos * y_pred_pos)
        tn = K.sum(y_neg * y_pred_neg)
        fp = K.sum(y_neg * y_pred_pos)
        fn = K.sum(y_pos * y_pred_neg)
        accuracy = (tp+tn)/(tp+tn+fp+fn)

        return accuracy

    def sensitivity(self, y_true, y_pred):
        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.round(K.clip(y_true, 0, 1))
        y_neg = 1 - y_pos
        tp = K.sum(y_pos * y_pred_pos)
        tn = K.sum(y_neg * y_pred_neg)
        fp = K.sum(y_neg * y_pred_pos)
        fn = K.sum(y_pos * y_pred_neg)
        sensitivity = tp/(tp+fn)

        return sensitivity

    def specificity(self, y_true, y_pred):
        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.round(K.clip(y_true, 0, 1))
        y_neg = 1 - y_pos
        tp = K.sum(y_pos * y_pred_pos)
        tn = K.sum(y_neg * y_pred_neg)
        fp = K.sum(y_neg * y_pred_pos)
        fn = K.sum(y_pos * y_pred_neg)
        specificity = tn/(tn+fp)

        return specificity
