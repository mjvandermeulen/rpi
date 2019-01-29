#!/usr/bin/env python

import os
import glob
from time import time  # for x axis plotting

import matplotlib.pyplot as plt

import automation_classes.temperature_reader as temperature_reader
import automation_classes.temperature_file_writer as temperature_file_writer


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

    """

    def __init__(self, target_temp, interval, filename):  # TODO: refactor to allow for celsius
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

        self.filename = filename
        self._writer = temperature_file_writer.TemperatureFileWriter(
            self.filename)

        # same as self._t_list[-1] but not redundant, since it's a public attribute and the list is not
        self.current_temp = 1000
        self.throttle = -1

        # current data
        self._integral = 0.0
        self._differential = 0.0

        # past (and current) data
        self._reading_count_list = []
        self._time_list = []
        self._t_list = []
        # self._p_list = []
        # self._i_list = []
        # self._d_list = []

        # plotting
        # plt.ion()  # interactive on
        # self._fig, self._ax = plt.subplots()

    def _write_to_file(self):
        reading_data = {
            'time_stamp': self._time_list[-1],
            'temp_stamp': self._t_list[-1],
            'throttle': float(self.throttle),
            'target_temp': float(self.target_temp),
            # error can be deduced
            'integral': float(self._integral),
            'differential': float(self._differential)
        }
        self._writer.write_temperature_reading(reading_data)

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

    def _update_integral(self, error, min_integral, max_integral):
        # measured in (F * sec): accumulation of error (F) over time (seconds)
        self._integral += error * self.interval
        if self._integral > max_integral:
            self._integral = max_integral
        if self._integral < min_integral:
            self._integral = min_integral
        return self._integral

    def _update_differential(self):
        """
        for crockpot:
            average of diff
            OF THE ERROR !!!
            with 2 minutes ago 4 minutes ago
            in Fahrenheit/ second.

            NOTE: the error is not recorded, so we're using the NEGATIVE diff of the temperature

        Returns
        -------
        float
            The differential
        """

        t = self._t_list[-1]
        # -1 is last reading
        # calculates steps back for 2 (#hardcoded) minutes:
        step1 = max(round(120 / self.interval), 1)
        # better than step2 = 2 * step1
        step2 = max(round(120 * 2 / self.interval), 1)

        n = len(self._t_list)
        if n < (step1 + 1):
            return 0.0
        elif n < (step2 + 1):
            step2 = step1

        # the differential of the ERROR is the OPPOSITE (negation) of the differential of the temperature:
        diff_step1 = -(
            (t - self._t_list[-1 - step1])
            / (step1 * self.interval)
        )
        diff_step2 = -(
            (t - self._t_list[-1 - step2])
            / (step2 * self.interval)
        )

        self._differential = (
            diff_step1 + diff_step2
        ) / 2
        return self._differential

    def _calculate_throttle(self):

        # TODO: move to init or even better: to temp_control_settings.py
        k_p = 0.5
        # integral is error (in F) times time (s). OLD: 0.05 -> 0.0008333333 say 0.0008
        k_i = 0.0005  # seems like a good value, not tested yet Jan 28.
        # differential is measured in Fahrenheit per second (F/s, like velocity in distance over time graph)
        k_d = 100  # 120 was working. Let's try 100.

        # TODO: think about this value. This only needs to be this high if you cook something just above room temp :) Kombucha?
        min_i = -1 / k_i

        # (full throttle, at level (d == 0) target temperature (p == 0). Tinkering possible here.)
        max_i = 1 / k_i

        # the error is positive if the current temperature is below the target temperature.
        # THE ERROR IS THE DEGREES TO GO UP TO THE TARGET TEMPERATURE.
        error = self.target_temp - self.current_temp
        self._update_integral(error, min_i, max_i)
        i = self._integral
        self._update_differential()
        d = self._differential

        print("target:  {:14.8f}".format(self.target_temp))
        print("temp:    {:14.8f}".format(self.current_temp))
        print()
        print("error:   {:14.8f}".format(error))
        print("i:       {:14.8f}".format(i))
        print("d:       {:14.8f}".format(d))

        print()

        # the bigger the error the more throttle
        p_part = k_p * error
        # Python 3.6 (not on RPi yet):
        # print(f"p_part:  {p_part:14.8f}") # NOTE: both 'f's
        print("p_part:  {:14.8f}".format(p_part))
        # the bigger the buildup of errors over time the more throttle
        i_part = k_i * i
        print("i_part:  {:14.8f}".format(i_part))
        # the more the error increases the more throttle
        d_part = k_d * d
        print("d_part:  {:14.8f}".format(d_part))

        print()
        pid = p_part + i_part + d_part
        print("pid:     {:14.8f}".format(pid))

        throttle = pid
        if throttle < -1:
            throttle = -1
        if throttle > 1:
            throttle = 1
        print("throttle:{:14.8f}".format(throttle))
        return throttle

    def read_temp_f(self):
        t = self._temp_reader.read_temp_f()
        self.current_temp = t
        self._t_list.append(t)
        self._time_list.append(time())
        self.throttle = self._calculate_throttle()
        self._write_to_file()
        return t
