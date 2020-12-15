#!/usr/bin/env python

import sys
import time
import power_control.powertail

### settings ###
pin_mode = "BCM"
power_pin = 23

# create instance of PowerTail
power = power_control.powertail.PowerTail(pin_mode, power_pin, False)

number_of_blinks = 5
if len(sys.argv) > 1:
    number_of_blinks = int(sys.argv[1])

for i in range(number_of_blinks):
    print("step {:3d}".format(i))
    print("POWER ON")
    power.turn_on()
    time.sleep(3)
    print("POWER OFF")
    power.turn_off()
    time.sleep(3)
