#!/usr/bin/env python3

import time

import automation_classes.temperature as temperature

temp = temperature.Temperature(150, 60)

while True:
    t = temp.read_temp_f()
    print("=== start ===")
    print("The current temperature is {:5.1f} degrees Fahrenheit.".format(t))
    print("plotting...")
    temp.plot()
    print("end plotting for now")
    print("=== end ===")
    time.sleep(1)
