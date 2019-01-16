#!/usr/bin/env python

import sys
import RPi.GPIO as io

io.setmode(io.BCM)
power_pin = 23

io.setup(power_pin, io.OUT)
io.output(power_pin, False)

print()
print()
print("POWER ON.")
print()
print()

io.output(power_pin, True)
