#!/usr/bin/env python

import automation_classes.powertail as powertail

### settings ###
pin_mode = "BCM"
power_pin = 23

print()
print()
print("POWER ON.")
print()
print()

# create instance of PowerTail
power = powertail.PowerTail(pin_mode, power_pin, True)
