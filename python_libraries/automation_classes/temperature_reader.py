#!/usr/bin/env python3

import os
import glob

# time module needed to read until you find a proper temperature TODO: this is not so good.
# TODO change name to probe_temperature_reader or probe_temperature_sensor
import time


class TemperatureReader(object):
    """
    reads current temperature from probe
    see adafruit https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

    Methods:
    --------
    read_f(): float
        reads the current temperature in Fahrenheit.

    read_c(): float
        reads the current temperature in Celsius.
    """

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        self._base_dir = '/sys/bus/w1/devices/'
        self._device_folder = glob.glob(self._base_dir + '28*')[0]
        self._device_file = self._device_folder + '/w1_slave'

    def _read_temp_raw(self):
        """

        Returns
        -------
        lines: [type]?
            [description]?
        """
        f = open(self._device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_temp_1000(self):
        lines = self._read_temp_raw()
        # TODO if else, or TRY CATCH
        # serious potential for hanging here
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]

        return float(temp_string)

    def read_temp_c(self):
        return self._read_temp_1000() / 1000

    def read_temp_f(self):
        return (self._read_temp_1000() / 1000) * 9.0 / 5.0 + 32.0
