#!/usr/bin/env python3

import pickle
import csv

generic_profile = 'generic'
path_to_csv_automation = '../csv_automation'

# http://stackoverflow.com/a/28745948


def read_temperature_control_data_from_file_pickle_generator(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def read_temperature_profile(filename, profile_name=generic_profile, path=path_to_csv_automation):
    with open(path + '/' + filename) as profile_file:
        csv_dict_reader = csv.DictReader(profile_file, delimiter=',')
        profile = []
        match_found = False
        for row in csv_dict_reader:
            # for key in row:
            #     print("key: ==={}===".format(key))
            # if row["skip"]:  # TODO I get a key error here
            #     continue
            if (row["name"].lower() == profile_name.lower() or
                    (match_found and row["name"] == "")):
                match_found = True  # or remains True
                print("bingo")
                profile.append(row)
            elif row["name"].lower != profile_name.lower and match_found:
                break
    return profile
