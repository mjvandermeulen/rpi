#!/usr/bin/env python3

import time

from automation_classes import temperature as temperature
from automation_classes import powertail as powertail

target_temp = 180
interval = 6


temp = temperature.Temperature(target_temp, interval)
power = powertail.PowerTail('BCM', 23, False)

try:
    while True:
        print("=== start ===")
        t = temp.read_temp_f()
        throttle = temp.throttle
        print("throttle: {:7.5f}".format(throttle))
        print(
            "The current temperature is {:5.1f} degrees Fahrenheit.".format(t))
        temp.plot()

        # power control
        power.turn(throttle > 0)  # TODO flip sign!!!!!
        print("=== end ===")
        time.sleep(interval)

except KeyboardInterrupt:
    print("keyboard interrupt")
    temp.detach_plot()
    # program halts here
