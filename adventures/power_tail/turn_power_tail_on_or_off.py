#!/usr/bin/env python

import power_control.powertail
import sys

### settings ###
pin_mode = "BCM"
power_pin = 23  # default

if len(sys.argv) > 1 and 'n' in sys.argv[1]:
    power_on = True
    if len(sys.argv) > 2:
        try:
            boo = int(sys.argv[2])
        except:
            raise Exception('second argument (PIN) needs to be an integer')
else:
    power_on = False

print()

# create instance of PowerTail
power = power_control.powertail.PowerTail(pin_mode, power_pin, power_on)

print()
if power_on:
    print("POWER ON")
else:
    print("POWER OFF")
print()
