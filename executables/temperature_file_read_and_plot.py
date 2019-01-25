#! /usr/bin/env python3

import sys
import matplotlib.pyplot as plt

from automation_modules import temperature_file_tools as temperature_file_tools

plt.ion()

try:
    data_file = sys.argv[1]
except IndexError:
    print("no filename provided as first and only argument")
else:  # if no exceptions:
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
                integral = []
                differential = []
                target_temp = []
                throttle = []
                for data in generator_of_dicts:
                    temp_stamp.append(data["temp_stamp"])
                    x_time.append(data["time_stamp"] / 3600.0)
                    integral.append(data["integral"] + data["target_temp"])
                    differential.append(
                        data["differential"] + data["target_temp"])
                    target_temp.append(data["target_temp"])
                    throttle.append(data["throttle"] * 10
                                    + data["target_temp"])
                # pylint:disable=all
                plt.plot(x_time, temp_stamp, 'b', label="temp in F")
                plt.plot(x_time, integral, 'y', label='Integral', marker='o')
                plt.plot(x_time, differential, 'r', label='Differential')
                plt.plot(x_time, target_temp, 'b', label='Target Temp')
                plt.plot(x_time, throttle, 'r', label='Throttle')
                plt.legend()
                plt.show(block=True)
                # block=True only needed if
                # plt.ion()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
