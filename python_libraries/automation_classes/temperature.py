#!/usr/bin/env python

import os
import glob

import matplotlib.pyplot as plt


class temperature (object):
    """
    This class:
    - FOR NOW ALL IN FAHRENHEIT. otherwise it'll get messed up.
    - reads the temperature
    - remembers the previously read temperatures in a list.
    - calculates the throttle needed to reach set temperature (from -1 to 1)
    - has a method for plotting.

    Attributes
    ----------
    interval: int
        time in seconds between readings (not enforced, since timing is up to the caller of the class methods)
    current_temp_f: float
        current (last read) temperature in Fahrenheit
    current_temp_c: float
        current (last read) temperature in Celsius
    throttle: float
        throttle needed to reach the set temperature from -1 to 1

    Methods
    -------
    read_temp_f(): float
        reads the temperature and stores this data.
        Triggers recalculation of the throttle.
        returns the read temperature

    plot()
        plots the list data.

    write_to_csv_file(filename = "temperature")
        writes to "[temperature] [timestamp].csv"
        e.g.: "temperature 2019 01 21 18:27.csv"
        creates this file if it does not exist.
        writes the following columns:
        HEADER?
        - temperature in fahrenheit
        - throttle
        - p proportion(al)
        - i integral
        - d derivative
    """

    def __init__(self, target_temp, interval):  # TODO: refactor to allow for celsius
        """ 
        initializes temperature object.
        NOTE: does not need the filename, this needs to be given everytime the write() method is called.

        Parameters
        ----------
        target_temp : int
            target temperature in Fahrenheit
        interval : int, optional
            time in seconds between readings (the default is 60, which [default_description])

        """

        self.target_temp = target_temp
        self.interval = interval

        self.current_temp_f = 1000
        self.current_temp_c = 1000
        self.throttle = -1

        self._integral = 0

        self._x_plot = []
        self._y_plot = []
        plt.ion()  # interactive on

    def read_temp_f(self):
        print("place call to temperature_reader here")

    def plot(self):
        """
        plot the current data (not the data that is written to file)

        """
        # FIRST IMPLEMENT READ TEMP
        #   AND APPEND X AND Y VALUES THERE.
