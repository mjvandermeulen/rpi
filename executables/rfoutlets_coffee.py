#!/usr/bin/env python

# EQUAL PARTS VINEGAR AND WATER
#
# https://www.goodhousekeeping.com/home/cleaning/tips/a26565/cleaning-coffee-maker/
#
# Fill the reservoir with equal parts vinegar and water, and place a paper filter
# into the machine's empty basket. Position the pot in place, and "brew" the solution
# halfway. Turn off the machine, and let it sit for 30 minutes. Then, turn the
# coffee maker back on, finish the brewing, and dump the full pot of vinegar and water.
# Rinse everything out by putting in a new paper filter and brewing a full pot
# of clean water. Repeat once.

# settings:

import time
from python_libraries.automation_modules import rfoutlets as rfo
import argparse
cycles = 30
brew = 20  # seconds
pause = 15 * 60  # seconds


cleaning_instructions = "Add vinegar and water 1 : 1 in coffeemaker. Fill MrCoffee to 12 cups when using default settings."

try:
    parser = argparse.ArgumentParser(
        description="TODO")
    parser.add_argument("outlet_group")

    parser.add_argument('--delay', '-d',
                        type=float, default=0.1,
                        metavar='hours')
    parser.add_argument('--clean', '-c',
                        action='store_true',
                        help='use TMUX when running a cleaning cycle')
    parser.add_argument('--rinse', '-r',
                        action='store_true',
                        help='rinse the coffeepot after the cleaning cycle')
    parser.add_argument('--pytest',
                        action="store_true",
                        help='used by pytest, to run a quicker test'
                        )

    args = parser.parse_args()
    if args.pytest:
        cycles = 1
        brew = 0.5  # seconds
        pause = 10  # seconds
    args_dict = vars(args)
    for key in args_dict:
        print(key + ' -> ' + str(args_dict[key]))

    total_hours = (
        args.delay +
        (pause * (cycles - 1) + brew * cycles) / (60.0 * 60.0)
    )

    print
    print(cleaning_instructions)

    print
    print("The brewing process will start in {:.2f} hours, and will be finished {:.2f} hours from now...".format(
        args.delay, total_hours))

    time.sleep(args.delay * 60 * 60)

    rv = ''
    for i in range(cycles):
        # PAUSE
        if i > 0:
            time.sleep(pause)

        # BREW
        print
        print("brew cycle {:2d}".format(i+1))
        rv = rfo.switch_outlet_group(args.outlet_group, 'on', 3, 2)
        if rv:
            print(rv)
        else:
            print('error')
        time.sleep(brew)
        rv = rfo.switch_outlet_group(args.outlet_group, 'off', 3, 2)
        if rv:
            print(rv)
        else:
            print('error')

except KeyboardInterrupt:
    rfo.switch_outlet_group(args.outlet_group, 'off')
    print
    print("KeyboardInterrupt")
    print
except Exception as error:
    rfo.switch_outlet_group(args.outlet_group, 'off')
    print
    print("An error occured. I'm super sorry: ")
    print("error: ")
    print(error)
    print
else:
    print
    print("DONE, no exceptions")
