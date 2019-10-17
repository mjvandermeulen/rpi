#!/usr/bin/env python


import sys
import time
from python_libraries.automation_modules import rfoutlets as rfo


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

# Arguments:
# 1: group
# 2: mode (on/off)
# 3: number of attempts

if len(sys.argv) > 2:
    outlet_group = sys.argv[1]
    mode = sys.argv[2]
    if len(sys.argv) > 3:
        attempts = int(sys.argv[3])
    else:
        attempts = 3

    rv = ''
    for i in range(attempts):
        if i > 0:
            time.sleep(2)
        rv = rfo.switch_outlet_group(outlet_group, mode)
    if rv:
        print(rv)
    else:
        print('error')
else:
    print('usage example:')
    print('./rfoutlets_switch_group.py basem n 2\n')
    print('2 arguments required')
    print('group')
    print('mode (e.g.: on)')
    print('1 optional argument:')
    print('number of attempts')
