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


import time
import argparse
import collections
import math

# from settings.automation_settings import AUTOMATION_EXECUTABLES_PATH
from remote_frequency_outlets import rfoutlets as rfo
from settings import automation_settings

# schedule_brew(args.outlet_group, schedule_time, settings.brew_time,)


def schedule_brew(group, minutes_from_now, brew_time):
    mode = 'off'  # final state
    attempts = 3
    delay = 1
    blink = (1, brew_time, 0)
    time_string = 'now + {} minute'.format(int(math.ceil(minutes_from_now)))
    rfo.rfo_schedule(time_string, group, mode, minutes_from_now,
                     attempts, delay, blink)


settings = automation_settings.coffee_settings["default"]

cleaning_instructions = "Add vinegar and water 1 : 1 in coffeemaker. Fill MrCoffee to 12 cups when using default settings."

try:
    parser = argparse.ArgumentParser(
        description="Mr Coffee 12 cup coffeemaker programmer using a remote frequency outlet.")
    parser.add_argument("outlet_group")

    parser.add_argument('--delay', '-d',
                        help='delay start of brewing in minutes',
                        type=float, default=automation_settings.coffee_default_delay,
                        metavar='min')
    maintenance_group = parser.add_mutually_exclusive_group()
    maintenance_group.add_argument('--clean', '-c',
                                   action='store_true',
                                   help='cleaning cycle for full 12 cup MrCoffee 1/2 vinegar 1/2 water')
    maintenance_group.add_argument('--rinse', '-r',
                                   action='store_true',
                                   help='rinse the coffeepot after the cleaning cycle')
    maintenance_group.add_argument('--test',
                                   action="store_true",
                                   help='used by pytest, to run a quicker test'
                                   )

    args = parser.parse_args()
    if args.test:
        settings = automation_settings.coffee_settings["test"]
    elif args.clean:
        settings = automation_settings.coffee_settings["clean"]
    elif args.rinse:
        settings = automation_settings.coffee_settings["rinse"]

    args_dict = vars(args)
    for key in args_dict:
        print(key + ' -> ' + str(args_dict[key]))

    total_hours = (
        args.delay * 60 +
        (settings.pause * (settings.cycles - 1) +
         settings.brew_time * settings.cycles) / (60.0 * 60.0)
    )

    print
    print(cleaning_instructions)

    print
    print("The brewing process will start in {:3d} minutes, and will be finished {:.2f} hours from now...".format(
        args.delay, total_hours))

    rv = ''
    schedule_time = args.delay * 60

    for i in range(settings.cycles):
        # PAUSE
        if i > 0:
            schedule_time += settings.pause

        # BREW:
        minutes_from_now = int(math.ceil(schedule_time / 60))
        if settings.brew_time < 3 * 60:
            # schedule once and use 1 blink for length of brew
            schedule_brew(args.outlet_group, minutes_from_now,
                          settings.brew_time)
        else:
            # schedule twice: turn on and turn off
            rfo.rfo_schedule_in_minutes(
                args.outlet_group, 'on', minutes_from_now, 3, 1)
            minutes_from_now = int(math.ceil(
                (schedule_time + settings.brew_time) / 60))
            rfo.rfo_schedule_in_minutes(
                args.outlet_group, 'off', minutes_from_now, 3, 1)
        schedule_time += settings.brew_time


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
