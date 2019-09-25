from collections import defaultdict
import logging

class SequenceSample(object):
    def __init__(self, number_lines):
        self._number_lines = number_lines
        self._samples = defaultdict(list)
        self._observers = []

    @property
    def samples(self):
        return self._samples

    @property
    def number_lines(self):
        return number_lines

    # @samples.setter
    def set_samples(self, line_index, line):
        self._samples[line_index].append(line)
        if len(self._samples[line_index]) >= self._number_lines:
            for callback in self._observers:
                self._samples[line_index].insert(0,line_index)
                callback(self._samples[line_index])
            # I have to clear the list to start acummulating
            # other lines
            self._samples[line_index] = []

    def bind_to(self, callback):
        self._observers.append(callback)
