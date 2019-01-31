#!/usr/bin/env python

import os
import glob
from time import time  # for x axis plotting
import math

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

    """

    # TODO: refactor to allow for celsius
    def __init__(self, setpoint, interval=60, filename='temperature_readings'):
        """
        initializes temperature object.
        NOTE: does not need the filename, this needs to be given everytime the write() method is called.

        Parameters
        ----------
        setpoint : int
            target temperature in Fahrenheit
        interval : int, optional
            time in seconds between readings (the default is 60, which [default_description])

        """
        self._temp_reader = temperature_reader.TemperatureReader()

        self.setpoint = self._round_setpoint_to_possible_reading(setpoint)
        self.interval = max(interval, 30)  # at least 30 seconds for now.

        self.filename = filename
        self._writer = temperature_file_writer.TemperatureFileWriter(
            self.filename)

        # same as self._temp_f_list[-1] but not redundant, since it's a public attribute and the list is not
        self.current_temp_f = 1000
        self.throttle = -1

        # current data
        self._integral = 1100.0  # ***** ##### TEMP
        self._differential = 0.0

        # past (and current) data
        self._reading_count_list = []
        self._time_list = []
        self._temp_f_list = []
        # self._p_list = []
        # self._i_list = []
        # self._d_list = []

        # plotting
        # plt.ion()  # interactive on
        # self._fig, self._ax = plt.subplots()

    def _round_setpoint_to_possible_reading(self, setpoint):
        """
        cute function to make the setpoint match a possible reading from the temperature probe
        This way the temperature can reach the setpoint exactly and fluctuate around it.

        Parameters
        ----------
        setpoint : float
            the given setpoint, when initializing the object

        Returns
        -------
        float
            the setpoint rounded to the nearest possible reading from the probe.
        """

        sp = (setpoint - 32) * 5.0 / 9.0  # to Celsius
        sp = round(sp * 16)  # readings are in 16th of a degree Celsius
        # readings are whole numbers / 1000, so precision of 3 decimals.
        # The temp probe readings in celsius are rounded down!
        sp = math.floor(sp / 16.0 * 1000) / 1000
        sp = sp * 9.0 / 5.0 + 32
        return sp

    def _write_to_file(self):
        reading_data = {
            'time_stamp': self._time_list[-1],
            'temp_f': self.current_temp_f,
            'temp_c': self.current_temp_c,
            'throttle': float(self.throttle),
            'setpoint': float(self.setpoint),
            # error can be deduced
            'integral': float(self._integral),
            'differential': float(self._differential)
        }
        self._writer.write_temperature_reading(reading_data)

    def plot(self):
        """
            This has become obsolete, as I'm only plotting from file now.
            This is kept here to show live plotting, according to new methods (see links) Initially this was taken from a Pi project, but that no longer works.
        """
        # https://github.com/matplotlib/matplotlib/issues/7759#issuecomment-271110279
        # as well: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots.html

        # pylint: disable=no-member
        # x_list = [i for i in range(len(self._temp_f_list))] # list comprehesion
        x_list = list(range(len(self._temp_f_list)))

        self._ax.plot(x_list, self._temp_f_list)
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
            with 1 minutes ago (#hardcoded)
            in Fahrenheit/ second.

            NOTE: the error is not recorded, so we're using the NEGATIVE diff of the temperature

        Returns
        -------
        float
            The differential
        """

        t = self._temp_f_list[-1]
        # -1 is last reading
        # calculates how many readings to go back for 1 (#hardcoded) minutes:
        readings_back = max(round(60 / self.interval), 1)

        n = len(self._temp_f_list)
        if n < (readings_back + 1):
            return 0.0

        # the differential of the ERROR is the OPPOSITE (negation) of the differential of the temperature:
        self._differential = -(
            (t - self._temp_f_list[-1 - readings_back])
            / (readings_back * self.interval)
        )

        return self._differential

    def _calculate_throttle(self):

        # TODO: move to init or even better: to temp_control_settings.py
        k_p = 0.5

        # integral is error (in F) times time (s). OLD: 0.05 -> 0.0008333333 say 0.0008
        # seems like a good value, not tested yet Jan 28. 0.0005 TEsted and working great. Slight fluctuation, but in bounds.
        k_i = 0.0005

        # differential is measured in Fahrenheit per second (F/s, like velocity in distance over time graph)
        # 120 was working. Now 100, but since only measure one minute back, this is a little much. (still working wonderfully though)
        k_d = 60

        # TODO: think about this value. This only needs to be this high if you cook something just above room temp :) Kombucha?
        min_i = -1 / k_i

        # (full throttle, at level (d == 0) target temperature (p == 0). Tinkering possible here.)
        max_i = 1 / k_i

        # the error is positive if the current temperature is below the target temperature.
        # THE ERROR IS THE DEGREES TO GO UP TO THE TARGET TEMPERATURE.
        error = self.setpoint - self.current_temp_f
        self._update_integral(error, min_i, max_i)
        i = self._integral
        self._update_differential()
        d = self._differential

        print("target:  {:14.8f}".format(self.setpoint))
        print("temp f:  {:14.8f}".format(self.current_temp_f))
        print("temp c:  {:14.8f}".format(self.current_temp_c))
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
        self.current_temp_c = self._temp_reader.read_temp_c()
        self.current_temp_f = self.current_temp_c * 9.0 / 5.0 + 32
        self._temp_f_list.append(self.current_temp_f)
        self._time_list.append(time())
        self.throttle = self._calculate_throttle()
        self._write_to_file()
        return self.current_temp_f
