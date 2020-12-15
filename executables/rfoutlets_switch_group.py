#!/usr/bin/python3


import time
import argparse

from remote_frequency_outlets import rfoutlets as rfo


class CustomError(Exception):  # exception raised for testing purposes.... :(
    pass


# thoughts:
# rfoutlets contains functions to
# actually switch the outlet (already true)
# meulen_automation contains the info about groups.
#
#
# @todo: allow multiple groups: NO, call repeatedly.

# Transmitter module
# DATA (left pin) -> GPIO #17
# VCC (center pin) -> +5VDC
# GND (right pin) -> Ground
#
# Receiver Module
# VCC (left pin) -> +5VDC
# DATA (2nd pin from left) -> GPIO 21/27
# GND (far right pin) -> Ground

# Arguments: TODO use argparse with multiple string values as input.
# but --attempts
# and --delay
# and --blinks
# 1: group
# 2: mode (on/off)
# 3: number of attempts

parser = argparse.ArgumentParser(description="TODO")
parser.add_argument('arguments', metavar='ARG', nargs='+',
                    help='arguments for remote frequency outlet, e.g. rfo 10 on in 5 minutes --blinks 10 --length 5')
parser.add_argument('--attempts', '-a',
                    help='attempts',
                    type=int)
parser.add_argument('--delay', '-d',
                    help='delay between attempts',
                    type=int)
parser.add_argument('--blinks', '-b',
                    help='blinks',
                    type=int)
parser.add_argument('--blinkon', '-n',
                    help='seconds length of blink on',
                    type=int)
parser.add_argument('--blinkoff', '-f',
                    help='seconds length of blink off',
                    type=int)
args = parser.parse_args()
args_dict = vars(args)
for key in args_dict:
    print(key + ' -> ' + str(args_dict[key]))

# TODO make mode = 'blink' archaic: use on or off for final state only TODO ***

if len(args.arguments) > 1:
    outlet_group = args.arguments[0]
    mode = args.arguments[1]

    rv = ''
    rv = rfo.switch_outlet_group(
        outlet_group, mode, args.attempts, args.delay, (args.blinks, args.blinkon, args.blinkoff))
    if rv:
        print(rv)
    else:
        # exception raised for testing purposes.... :(
        raise CustomError('no outlets switched')
else:
    print('usage example:')
    print('./rfoutlets_switch_group.py basem n 2\n')
    print('2 arguments required')
    print('group')
    print('mode (e.g.: on)')
