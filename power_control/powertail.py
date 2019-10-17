#!/usr/bin/env python

# Black wire from power tail goes to ground
# White wire from power tail goes to "pin" (BCM 23 is often a good option for mjvandermeulen)
#   depending on setmode:
#     BOARD: numbers 1..40 (even on one side, odd on the other)
#     BCM: (PREFERRED!) "names" printed on cobbler. On Cana Kit Card: GPIO 23 --> pin = 23

import RPi.GPIO as GPIO
from time import sleep as sleep


class PowerTail(object):
    """
    a Class by mjvandermeulen
    representing the output of the powertail and methods to change the output
    Upon initialization turns the ouput to initial_output (True or False)
    Created instance remembers the output in attribute: .output

    NOTE: "on" or "off" are never used as parameters, only True and False

    Attributes
    ----------
    output : bool
        True if powertail is on, False if off

    Methods
    -------
    turn(output=False)
        Turns the power to True, or False
    turn_on()
    turn_off()
    toggle()
    """

    def __init__(self, gpio_mode, pin, initial_output):
        """
        Parameters
        ----------
        gpio_mode : string
            "BCM" (preferred) or "BOARD"
        pin : int
            pin number (depending on gpio_mode)
        initial_output : bool
            True (on) or False (initially off)
        """

        print("init powertail instance")

        self.pin = pin
        print("  pin: {}".format(self.pin))
        if gpio_mode == "BOARD":
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, initial_output)
        self.output = initial_output
        print("on init turned powertail " +
              ("on" if initial_output else "off"))
        print("end init powertail instance")

    def turn(self, output=False):
        """
        Turn power to True (on) or False (off)

        Parameters
        ----------
        output : bool, optional
            True for powertail OFF, False for ON (the default is False, which sets the output pin to False)

        """
        if self.output == output:
            if output:
                print("staying on...")
            else:
                print("staying off...")
        else:
            if output:
                print("turning on...")
            else:
                print("turning off...")
            GPIO.output(self.pin, output)
            self.output = output

    def turn_on(self):
        """
        Turn power to True
        """
        if not self.output:
            print("turning on")
            GPIO.output(self.pin, True)
            self.output = True
        else:
            print("staying on")

    def turn_off(self):
        """
        Turn power to False
        """
        if self.output:
            print("turning off")
            GPIO.output(self.pin, False)
            self.output = False
        else:
            print("staying off")

    def toggle(self):
        """
        Toggle power (True -> False, or False to True)
        """
        if not self.output:
            print("toggling the power tail OFF")
            GPIO.output(self.pin, False)
            self.output = False
        else:
            print("toggling the power tail ON")
            GPIO.output(self.pin, True)
            self.output = True

    def run_throttled_power_interval(self, power, throttle, min_throttle, max_throttle, interval, min_switch_time):
        """
        Keep in here, since it's powertail specific: 
        what to do with the control_function value.
        (a device with multiple settings (say slow, normal and fast would have to interpret the u value differently))
        example:
        interval = 60 seconds
          throttle min_throttle: 0 seconds on 60 off
          throttle 0: 30 seconds on 30 off
          throttle max_throttle: 60 seconds on  0 off
        pass

        """
        if throttle < min_throttle:
            print("throttle below min setting. " + __file__)
            throttle = min_throttle
        if throttle > max_throttle:
            print("throttle above max setting. " + __file__)
            throttle = max_throttle

        time_on = int(round(
            ((throttle - min_throttle) / (max_throttle - min_throttle) * interval))
        )
        # don't allow switching for less than min_switch_time seconds
        if time_on != interval and time_on > interval - min_switch_time:
            time_on = interval - min_switch_time
        elif time_on != 0 and time_on < min_switch_time:
            time_on = min_switch_time

        time_off = interval - time_on

        if time_on > 0:
            self.turn_on()
            sleep(time_on)
        if time_off > 0:
            self.turn_off()
            sleep(time_off)
