#!/usr/local/bin/python3

import time

from automation_classes import temperature_reader
from automation_classes import temperature
from automation_classes import powertail
from automation_modules import temperature_file_tools


# MAIN

try:

    # TODO
    # read sys.argv

    # plot filename as arg (defaults to profile name) TODO
    # arg 1: profile name
    # arg 2: csv filename (add .csv if not present)
    # arg 3: cvs folder pathname (remove trailing '/')

    profile = temperature_file_tools.read_temperature_profile(
        'temperature_profiles.csv', 'ricecooker_investigation')  # hardcoded file name. # hardcoded profile name
    # for profile_stage in profile:
    #     for key in profile_stage:
    #         print("profile stage: profile_stage[\"{}\"] = {}".format(
    #             key, profile_stage[key]))

    temp_reader = temperature_reader.TemperatureReader()
    tc = temperature.Temperature(
        'cbd', appliance='crockpot')  # name only for plot filename.

    # init powertail
    power = powertail.PowerTail('BCM', 23, False)

    for profile_stage in profile:
        tc.set_profile_stage_params(profile_stage)

        t = start_of_stage = time.time()
        duration = int(float(profile_stage["duration"]) * 60 * 60)

        # for key in profile_stage:
        #     print("profile_stage[\"{}\"] = {}".format(
        #         key, profile_stage[key]))

        while t < start_of_stage + duration:
            print("===========================")
            print("=== start control loop  ===")
            print("===========================")

            temp_f = temp_reader.read_temp_f()

            tc.process_f_measurement(temp_f)

            # CLEANUP: parameters
            throttle = tc.throttle(tc.min_throttle, tc.max_throttle)

            # run power interval
            power.run_throttled_power_interval(
                power, throttle, -1, +1, tc.interval, tc.min_switch_time)
            print()
            print("=== end while loop in " + __file__ + " ===")
            print()
            # separate notification .csv file! (warnings, errors, and hourly updates)
            t = time.time()
except KeyboardInterrupt:
    power.turn_off()

else:
    print('ended, no exceptions')

finally:
    print('DONE ' + __file__)
