#!/usr/local/bin/env python3

import sys

# TODO: This is more generic than just for temperatures!
import temperature.temperature_file_tools

try:
    filename = sys.argv[1]
except IndexError:
    print("please provide filename as first and only argument")
else:
    try:
        data_gen = temperature.temperature_file_tools.read_temperature_control_data_from_file_pickle_generator(
            filename)
        data = next(data_gen)
        print("\nFirst Row:")
        for key in data:
            print("  data[{}] = {}".format(key, data[key]))
    except:
        print("Unable to open {} or parse the first data".format(filename))
