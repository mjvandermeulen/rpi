#!/usr/bin/env python3

import time
import pickle


class TemperatureFileWriter(object):
    """
    Creates writer object that initializes the filename, prepended with date and time.
    Offers writing method to write (or append)
    Keeps track of writing or appending mode, depending on first write or not.

    Attributes:
    -----------
    filename: str
        the date and time prepended actual filename

    Methods:
    --------
    write_temperature_reading(data)
        writes the data to the file
        data has to be in the correct dictionary form, see below.

    """

    def __init__(self, filename):
        ts = time.time()
        string_time = time.strftime(
            "%Y-%m-%d_%H-%M", time.localtime(ts))
        # example output: '2019 02 03 13:33'

        self.filename = filename + '_' + string_time + '.pickle'

        self._write_mode = 'wb'

    def write_temperature_reading(self, data):
        """
        writes dictionary data to file.

        Parameters
        ----------
        data : dictionary
            example:
            {
                'reading_number': reading_number,
                'time_stamp': time_stamp,
                'temp_f': temp_f,
                'throttle': float(throttle),
                ...
            }
        """
        with open(self.filename, self._write_mode) as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        self._write_mode = 'ab'
