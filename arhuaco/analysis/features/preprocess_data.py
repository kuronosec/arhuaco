import numpy as np
import re
import itertools
from collections import Counter
import pandas as pd

class PreprocessData:

    def clean_str(self, str_par):
        str_local = re.sub(r"[^A-Za-z0-9\.\/]", " ", str_par)
        return str_local

    def preprocess_chunk(self, chunk):
        # Split by words
        x_text = chunk.values.tolist()
        x_text = [self.clean_str(sent[0]) for sent in x_text]
        x_text = [s.split(" ") for s in x_text]
        return x_text

if __name__ == '__main__':
    from data_helpers import DataHelpers
    from preprocess_data import PreprocessData

    print("Loading data...")
    data_helper = data_helpers = DataHelpers(data_source=None,
                                 label=None,
                                 tokens_per_line=None,
                                 number_lines=None,
                                 samples_per_batch=None,
                                 seed=None)
    stream_nor = data_helper.get_stream(file="/var/lib/arhuaco/data/new_normal_ready.csv", chunk_size=100000)
    stream_mal = data_helper.get_stream(file="/var/lib/arhuaco/data/new_malicious_ready.csv", chunk_size=100000)
    prep_data = PreprocessData()
    i = 0
    for chunk_nor in stream_nor:
        chunk_mal = next(stream_mal)
        print("Processing data %d" % i)
        x_nor = prep_data.preprocess_chunk(chunk_nor)
        x_mal = prep_data.preprocess_chunk(chunk_mal)
        print("Saving data chunck %d" % i)
        data_nor = pd.DataFrame(x_nor)
        data_mal = pd.DataFrame(x_mal)
        data_nor.to_csv("/var/lib/arhuaco/data/new_normal_clean.csv", header=None, index=None, index_label=None, sep=' ', mode='a+')
        data_mal.to_csv("/var/lib/arhuaco/data/new_malicious_clean.csv", header=None, index=None, index_label=None, sep=' ', mode='a+')
        i = i + 1
