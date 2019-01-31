#!/usr/local/bin/env python3

import sys

# TODO: This is more generic than just for temperatures!
from automation_modules import temperature_file_tools

try:

    filename = sys.argv[1]

    try:
        data_gen = temperature_file_tools.read_temperature_control_data_from_file_pickle_generator(
            filename)
        data = next(data_gen)

        for key in data:
            print("data[{}] = {}".format(key, data[key]))
    except:
        print("Unable to open {} or parse the first data".format(filename))
except:
    print("please provide filename as first and only argument")
