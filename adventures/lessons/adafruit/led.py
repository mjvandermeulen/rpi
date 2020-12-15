#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

pins = {'red': 6}

GPIO.setmode(GPIO.BCM)
for color in pins:
    GPIO.setup(pins[color], GPIO.OUT)


def led(color, choice):
    if color in pins:
        # choices that evaluate as False:
        # False; 0; ""; "off" ("off" is manually added)
        choice = bool(choice and not choice == "off")
        print(color)
        print(pins[color])
        if choice:
            print("on")
        else:
            print("off")
        GPIO.output(pins[color], choice)
    else:
        print("the color " + color + " is not in the dictionary.")


def all_leds_off():
    for color in pins:
        led(color, False)


try:
    while True:
        led("red", True)
        time.sleep(1)
        led("red", False)
        time.sleep(1)

except KeyboardInterrupt:
    all_leds_off()

finally:
    print("bye bye")
