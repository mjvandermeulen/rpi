#!/usr/bin/env python

import sys
import RPi.GPIO as io

io.setmode(io.BCM)
power_pin = 23

io.setup(power_pin, io.OUT)
io.output(power_pin, True)

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
io.output(power_pin, power_on)


print()
print()
