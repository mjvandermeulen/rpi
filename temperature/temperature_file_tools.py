#!/usr/bin/env python3

import pickle
import csv

generic_profile = 'generic'
path_to_csv_automation = '../csv_automation'


def read_temperature_control_data_from_file_pickle_generator(filename):
    """
    TODO: make totally generic!!! put in tools/file/pickle_reader.py

    about pickle generators:
    http://stackoverflow.com/a/28745948
    """
    try:
        with open(filename, 'rb') as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break
    except IOError:
        print("file {} not found in read_temperature_control_data_from_file_pickle_generator".format(filename))


def read_temperature_profile(filename, profile_name=generic_profile, path=path_to_csv_automation):
    """
    Excel saves as UTF-8, see encoding='utf-8-sig'
    """

    with open(path + '/' + filename, encoding='utf-8-sig') as profile_file:
        csv_dict_reader = csv.DictReader(profile_file, delimiter=',')
        profile = []
        match_found = False
        for row in csv_dict_reader:
            if row["skip"]:
                continue
            if (row["name"].lower() == profile_name.lower() or
                    (match_found and row["name"] == "")):
                match_found = True  # or remains True
                profile.append(row)
            elif match_found and (row["name"].lower() != profile_name.lower() or not row["setpoint"]):
                break
    return profile
