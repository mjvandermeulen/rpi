#!/usr/bin/env python

import sys
import time
import RPi.GPIO as io

io.setmode(io.BCM)
power_pin = 23

io.setup(power_pin, io.OUT)
io.output(power_pin, False)

number_of_blinks = 5
if len(sys.argv) > 1:
    number_of_blinks = int(sys.argv[1])

print("POWER ON")
io.output(power_pin, True)
time.sleep(1)


for i in range(number_of_blinks):
    print ("step {:3d}".format(i))
    print("POWER OFF")
    io.output(power_pin, False)
    time.sleep(3)
    print("POWER ON")
    io.output(power_pin, True)
    time.sleep(3)
