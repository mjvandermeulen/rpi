#!/usr/bin/env python

import automation_classes.powertail as powertail
import sys

### settings ###
pin_mode = "BCM"
power_pin = 23

# create instance of PowerTail
power = powertail.PowerTail(pin_mode, power_pin, False)
if len(sys.argv) > 1 and 'n' in sys.argv[1]:
    power_on = True
else:
    power_on = False

print()
print()

if power_on:
    print("POWER ON")
else:
    print("POWER OFF")
power.turn(power_on)

print()
print()
