#!/usr/bin/env python3

import time

from automation_classes import temperature as temperature
from automation_classes import powertail as powertail

target_temp = 179
interval = 60  # seconds
# Just to make sure the powertail is not switching after just one second... NEEDED?
min_switch_time = 2

# TODO ##### move to args
temp = temperature.Temperature(target_temp, interval, 'test-after-cbd')
power = powertail.PowerTail('BCM', 23, False)


def run_throttled_power_interval(power, throttle, interval):
    """
    move to powertail class? with min and max throttle

    Parameters
    ----------
    power : Powertail
        obviously would not be needed when this becomes a method of that class
    throttle : [type]
        [description]
    interval : [type]
        [description]

    """

    # example:
    # interval = 60 seconds
    #   throttle -1: 0 seconds on 60 off
    #   throttle 0: 30 seconds on 30 off
    #   throttle 1: 60 seconds on  0 off
    # pass
    time_on = int(round(((throttle + 1) / 2) * interval))
    if time_on != interval and time_on > interval - min_switch_time:
        time_on = interval - min_switch_time
    elif time_on != 0 and time_on < min_switch_time:
        time_on = min_switch_time

    time_off = interval - time_on
    if time_on > 0:
        power.turn_on()
        time.sleep(time_on)
    if time_off > 0:
        power.turn_off()
        time.sleep(time_off)


try:
    while True:
        print()
        print("=== start while loop in " + __file__ + " ===")
        print()
        temp.read_temp_f()
        throttle = temp.throttle

        # temp.plot()

        # power control
        run_throttled_power_interval(power, throttle, interval)
        print()
        print("=== end while loop in " + __file__ + " ===")
        print()

except KeyboardInterrupt:
    print("keyboard interrupt")
    power.turn_off()
    temp.detach_plot()
    # program halts here
