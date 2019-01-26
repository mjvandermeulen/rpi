#!/usr/bin/env python3

import time

from automation_classes import temperature as temperature
from automation_classes import powertail as powertail

target_temp = 200
interval = 60  # seconds


temp = temperature.Temperature(target_temp, interval, '180cbd')
power = powertail.PowerTail('BCM', 23, False)


def run_throttled_power_interval(power, throttle, interval):
    # example:
    # interval = 60 seconds
    #   throttle -1: 0 seconds on 60 off
    #   throttle 0: 30 seconds on 30 off
    #   throttle 1: 60 seconds on  0 off
    # pass
    time_on = int(round(((throttle + 1) / 2) * interval))
    time_off = interval - time_on
    if time_on > 0:
        power.turn_on()
        time.sleep(time_on)
    if time_off > 0:
        power.turn_off()
        time.sleep(time_off)


try:
    while True:
        print("=== start while loop in " + __file__ + " ===")
        t = temp.read_temp_f()
        throttle = temp.throttle
        print("throttle: {:7.5f}".format(throttle))
        print(
            "The current temperature is {:5.4f} degrees Fahrenheit.".format(t))
        # temp.plot()

        # power control
        run_throttled_power_interval(power, throttle, interval)
        print("=== end while loop in " + __file__ + " ===")

except KeyboardInterrupt:
    print("keyboard interrupt")
    power.turn_off()
    temp.detach_plot()
    # program halts here
