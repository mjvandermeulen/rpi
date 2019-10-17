#!/usr/local/bin/python3

import time

import temperature
import power_control.powertail


# MAIN

try:

    # TODO
    # read sys.argv

    profile_name = 'test-feb'  # hardcoded

    # plot filename as arg (defaults to profile name) TODO argparse
    # arg 1: profile name
    # arg 2: csv filename (add .csv if not present)
    # arg 3: cvs folder pathname (remove trailing '/')

    profile = temperature.temperature_file_tools.read_temperature_profile(
        'temperature_profiles.csv', profile_name=profile_name)  # hardcoded file name.
    for profile_stage in profile:
        print("profile stage setpoint: {}".format(profile_stage["setpoint_f"]))
        # for key in profile_stage:
        #     print("profile stage: profile_stage[\"{}\"] = {}".format(
        #         key, profile_stage[key]))

    temp_reader = temperature.temperature_reader.TemperatureReader()
    tc = temperature.temperature_controller.TemperatureController(
        plot_file=profile_name,
        appliance='crockpot')  # hardcoded appliance # hardcoded profile (used for plot_file name)

    # init powertail
    power = power_control.powertail.PowerTail('BCM', 23, False)

    for profile_stage in profile:
        print("=======================================================================")
        print("=== start profile_stage ===============================================")
        print("=======================================================================")
        tc.set_profile_stage_params(profile_stage)

        t = start_of_stage = time.time()
        duration = int(float(profile_stage["duration"]) * 60 * 60)

        # for key in profile_stage:
        #     print("profile_stage[\"{}\"] = {}".format(
        #         key, profile_stage[key]))

        while t < start_of_stage + duration:
            print("=== start control loop  ===")

            temp_f = temp_reader.read_temp_f()

            tc.process_f_measurement(temp_f)

            throttle = tc.throttle()
            print("throttle:{:14.8f}".format(throttle))

            # run power interval
            power.run_throttled_power_interval(
                power, throttle, tc.min_throttle, tc.max_throttle, tc.interval, tc.min_switch_time)
            print()
            print("=== end while loop in " + __file__ + " ===")
            print()
            # separate notification .csv file! (warnings, errors, and hourly updates)
            t = time.time()
except KeyboardInterrupt:
    print()
    print("KeyboardInterrupt")
    print()

else:  # if no exceptions (read: if exception do yada yada, else ...)
    print('ended, no exceptions')

finally:  # always (exceptions or not)
    print()
    power.turn_off()
    print('DONE ' + __file__)
