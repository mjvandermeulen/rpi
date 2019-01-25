#!/usr/bin/env python3

import pickle

# http://stackoverflow.com/a/28745948


def read_temperature_control_data_from_file_pickle_generator(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
