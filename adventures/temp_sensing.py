#!/usr/bin/env python3

import time

import automation_classes.temperature_reader as t_reader

temp_reader = t_reader.TemperatureReader()

while True:
    t = temp_reader.read_temp_f()
    print("The current temperature is {:5.1f} degrees Fahrenheit.".format(t))
    time.sleep(1)
