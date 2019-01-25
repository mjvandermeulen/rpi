#! /usr/bin/env python3

import sys
import pickle


first_dict = {}

try:
    data_file = sys.argv[1]
except IndexError:
    print("no filename proviced as first and only argument")
else:  # if no exception
    try:
        with open(data_file, 'rb') as f:
            try:
                first_dict = pickle.load(f)
            except EOFError:
                print("no dictionary found")
    except IOError:
        print("No such file.")
    else:
        for key in first_dict:
            print(key)
