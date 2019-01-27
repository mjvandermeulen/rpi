#! /usr/bin/env python3

import sys
import matplotlib.pyplot as plt

from automation_modules import temperature_file_tools as temperature_file_tools

plt.ion()

k_i = 0.0008
try:
    data_file = sys.argv[1]
    if len(sys.argv) > 2:
        k_i = float(sys.argv[2])
except IndexError:
    print("no filename provided as first and only argument")
else:  # if no exceptions:
    print("k_i: {}".format(k_i))
    try:
        while True:
            try:
                generator_of_dicts = temperature_file_tools.read_temperature_control_data_from_file_pickle_generator(
                    data_file)
            except:
                print("file {} does not exist".format(data_file))
                break
            else:
                plt.title('Crock Pot temperatures over time (measurements')

                plt.xlabel('measurements')
                plt.ylabel('temperature in Fahrenheit mostly')

                x_time = []
                temp_stamp = []  # refactor to temp_f?
                error = []
                integral = []
                differential = []
                target_temp = []
                throttle = []
                for data in generator_of_dicts:
                    temp_stamp.append(data["temp_stamp"])
                    x_time.append(data["time_stamp"] / 3600.0)
                    integral.append(data["integral"] * k_i * 10
                                    + data["target_temp"])
                    # hardcoded k_d = 120
                    differential.append(data["differential"] * 120 * 10
                                        + data["target_temp"])
                    target_temp.append(data["target_temp"])
                    error.append(data["target_temp"] - data["temp_stamp"]
                                 + data["target_temp"])
                    throttle.append(data["throttle"] * 10
                                    + data["target_temp"])
                # pylint:disable=all
                plt.plot(x_time, temp_stamp, 'b', label="temp in F")
                # , marker='o')
                plt.plot(x_time, error, 'r', label='Error', linestyle='--')
                plt.plot(x_time, integral, 'y', label='Integral')
                plt.plot(x_time, differential, 'k', label='Differential')
                plt.plot(x_time, target_temp, 'k', label='Target Temp')
                plt.plot(x_time, throttle, 'g', label='Throttle')
                plt.legend()
                plt.show(block=True)
                # block=True only needed if
                # plt.ion()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
