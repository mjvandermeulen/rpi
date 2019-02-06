#!/usr/bin/env python

import os
import glob
import time
import math
import matplotlib.pyplot as plt

from automation_classes import temperature_file_writer
from automation_modules import automation_email  # OBSOLETE SOON
from automation_modules import temperature_file_tools
from automation_modules import automation_settings


class Temperature (object):
    """
    """
# TODO: change name to TemperatureController
# TODO: rename: profile (List) to profile_stages
# TODO: refactor to allow for celsius
# TODO: add 'generic'    def __init__(self, profile='generic', plot_file='temperature_readings'):

    def __init__(self, plot_file='temperature_readings', appliance='crockpot'):
        self.plot_file = automation_settings.tempcontroller_measurements_path + '/' + plot_file
        self._writer = temperature_file_writer.TemperatureFileWriter(
            self.plot_file)

        self.setpoint_f = -1000
        self._k_p = 0
        self._k_i = 0
        self._k_d = 0
        self._min_i = 0
        self._max_i = 0
        self._d_x = 0
        self.min_throttle = 0
        self.max_throttle = 0
        self.interval = 3600
        self.min_switch_time = 5

        # current data
        # same as self._temp_f_list[-1] but not redundant, since it's a public attribute and the list is not
        self.current_temp_f = 1000
        self._integral = 0.0
        self._differential = 0.0
        self.control_function_value = 0.0

        # past (and current) data
        self._time_list = []
        self._temp_f_list = []

        # plotting
        # plt.ion()  # interactive on
        # self._fig, self._ax = plt.subplots()

    def set_profile_stage_params(self, profile_stage):
        self.setpoint_f = float(profile_stage["setpoint_f"])
        self._k_p = float(profile_stage["k_p"])
        self._k_i = float(profile_stage["k_i"])
        self._k_d = float(profile_stage["k_d"])
        self._min_i = float(profile_stage["min_i"])
        self._max_i = float(profile_stage["max_i"])
        self._d_x = int(profile_stage["d_x"])
        self.min_throttle = float(profile_stage["min_throttle"])
        self.max_throttle = float(profile_stage["max_throttle"])
        self.interval = int(profile_stage["interval"])
        self.min_switch_time = int(profile_stage["min_switch_time"])

    def _round_setpoint_to_possible_reading(self, setpoint_f):
        """
        Not used currently?
        MAKE OBSOLETE: This method is too much tied into the temperature probe, or move to probe reader (give that probe reader a more specific name, with name of the probe (TCB 30 or someting like that))
        cute function to make the setpoint_f match a possible reading from the temperature probe
        This way the temperature can reach the setpoint_f exactly and fluctuate around it.

        Parameters
        ----------
        setpoint_f : float
            the given setpoint_f, when initializing the object

        Returns
        -------
        float
            the setpoint_f rounded to the nearest possible reading from the probe.
        """

        sp = (setpoint_f - 32) * 5.0 / 9.0  # to Celsius
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
            'throttle': float(self.throttle()),
            # important, since setpoint_f can change!
            'setpoint_f': float(self.setpoint_f),
            # error can be deduced
            'integral': float(self._integral),
            'differential': float(self._differential)
        }
        self._writer.write_temperature_reading(reading_data)

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

    def _calculate_control_function(self):

        # see https://en.wikipedia.org/wiki/PID_controller#Loop_tuning

        # the error is positive if the current temperature is below the target temperature.
        # THE ERROR IS THE DEGREES TO GO UP TO THE TARGET TEMPERATURE.
        error = self.setpoint_f - self.current_temp_f
        self._update_integral(error, self._min_i, self._max_i)
        i = self._integral
        self._update_differential()
        d = self._differential

        print("target:  {:14.8f}".format(self.setpoint_f))
        print("temp f:  {:14.8f}".format(self.current_temp_f))
        print("temp c:  {:14.8f}".format(self.current_temp_c))
        print()
        print("error:   {:14.8f}".format(error))
        print("i:       {:14.8f}".format(i))
        print("d:       {:14.8f}".format(d))

        print()

        # the bigger the error the more throttle
        p_part = self._k_p * error
        # Python 3.6 (not on RPi yet):
        # print(f"p_part:  {p_part:14.8f}") # NOTE: both 'f's
        print("p_part:  {:14.8f}".format(p_part))
        # the bigger the buildup of errors over time the more throttle
        i_part = self._k_i * i
        print("i_part:  {:14.8f}".format(i_part))
        # the more the error increases the more throttle
        d_part = self._k_d * d
        print("d_part:  {:14.8f}".format(d_part))

        print()
        # control function: u
        u = p_part + i_part + d_part
        print("u:       {:14.8f}".format(u))
        return u

    def throttle(self):
        u = self.control_function_value
        if u < self.min_throttle:
            return self.min_throttle
        if u > self.max_throttle:
            return self.max_throttle
        return u

    def process_f_measurement(self, temp_f):
        self.current_temp_f = temp_f
        self.current_temp_c = (temp_f - 32) * 5 / 9
        self._temp_f_list.append(self.current_temp_f)
        # ONLY Last value needed (like e.g.: current_temp_c_). NO LIST NEEDED
        self._time_list.append(time.time())
        self.control_function_value = self._calculate_control_function()
        self._write_to_file()
        return self.control_function_value

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
        This has become obsolete, as I'm only plotting from file now.
        This is kept here to show live plotting, according to new methods (see links) Initially this was taken from a Pi project, but that no longer works.

        call this method after keyboard interrupt
        in order to:
        - preserve the plot (otherwise the program would end and the plot would disappear)
        - halt the program, until the plot window is closed
        """

        plt.ioff()
        plt.show()
