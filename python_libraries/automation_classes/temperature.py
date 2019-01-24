#!/usr/bin/env python

import os
import glob
from time import time  # for x axis plotting

import matplotlib.pyplot as plt

import automation_classes.temperature_reader as temperature_reader


class Temperature (object):
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
    current_temp: float
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
        self._temp_reader = temperature_reader.TemperatureReader()

        self.target_temp = target_temp
        self.interval = interval

        # same as self._t_list[-1] but not redundant, since it's a public attribute and the list is not
        self.current_temp = 1000
        self.throttle = -1

        # current data
        self._integral = 0

        # past (and current) data
        self._reading_count_list = []
        self._time_list = []
        self._t_list = []
        # self._p_list = []
        # self._i_list = []
        # self._d_list = []

        # plotting
        plt.ion()  # interactive on
        self._fig, self._ax = plt.subplots()

    def plot(self):
        """
        plot the current data (not data from a file)
        """
        # https://github.com/matplotlib/matplotlib/issues/7759#issuecomment-271110279
        # as well: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots.html

        # pylint: disable=no-member
        # x_list = [i for i in range(len(self._t_list))] # list comprehesion
        x_list = list(range(len(self._t_list)))

        self._ax.plot(x_list, self._t_list)
        self._fig.canvas.flush_events()
        plt.draw()
        # pylint: enable=no-member

    def detach_plot(self):
        """
        call this method after keyboard interrupt
        in order to:
        - preserve the plot (otherwise the program would end and the plot would disappear)
        - halt the program, until the plot window is closed
        """

        plt.ioff()
        plt.show()

    def _update_integral(self, error):
        self._integral += error
        return self._integral

    def _calculate_diff(self):
        """
        average of diff with last reading (weighs double)
        and the diff with the reading before that.

        Returns
        -------
        float
            The differential
        """

        n = len(self._t_list)
        if n < 3:
            return 0.0

        t = self._t_list[-1]
        diff_prev_temp = t - self._t_list[-2]
        diff_prev_prev_temp = (t - self._t_list[-3]) / 2
        # give diff_prev_temp twice the weight
        return (
            (
                2 * diff_prev_temp
                + diff_prev_prev_temp
            ) / 3
        )

    def _calculate_throttle(self):

        # !!! A negative error means current_temp < target_temp
        error = self.current_temp - self.target_temp
        self._update_integral(error)
        i = self._integral
        d = self._calculate_diff()

        k_p = 0.5
        k_i = 0.1
        k_d = 2

        print("error: {:12.8}".format(error))
        print("i:     {:12.8}".format(i))
        print("d:     {:12.8}".format(d))

        print()

        p_part = k_p * -error
        print("p_part:  {:12.8}".format(p_part))
        i_part = k_i * -i
        print("i_part:  {:12.8}".format(i_part))
        d_part = k_d * -d
        print("d_part:  {:12.8}".format(d_part))

        pid = p_part + i_part + d_part

        if pid < -1:
            return -1
        if pid > 1:
            return 1
        return pid

    def read_temp_f(self):
        t = self._temp_reader.read_temp_f()
        self.current_temp = t
        self._t_list.append(t)
        self._time_list.append(time())  # not used yet... jan 23 2019
        self.throttle = self._calculate_throttle()
        return t
