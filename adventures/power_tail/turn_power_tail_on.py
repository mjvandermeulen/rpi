#!/usr/bin/env python

import power_control.powertail

### settings ###
pin_mode = "BCM"
power_pin = 23

print()
print()
print("POWER ON.")
print()
print()

# create instance of PowerTail
power = power_control.powertail.PowerTail(pin_mode, power_pin, True)
