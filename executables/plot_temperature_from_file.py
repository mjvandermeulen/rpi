#! /usr/local/bin/env python3

import sys
import matplotlib.pyplot as plt

from automation_modules import temperature_file_tools as temperature_file_tools

plt.ion()

k_i = 0.0005  # hardcoded
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
                x_time = []
                temp_f = []  # refactor to temp_f?
                error = []
                integral = []
                differential = []
                setpoint_f = []
                throttle = []
                first_time_stamp = 0
                for data in generator_of_dicts:
                    # unlikely that the first record was the first second in Jan 1 1970 (start of Unix time)
                    if first_time_stamp == 0:
                        first_time_stamp = data["time_stamp"]
                    x_time.append(
                        (data["time_stamp"] - first_time_stamp) / 3600.0)

                    temp_f.append(data["temp_f"])
                    integral.append(data["integral"] * k_i)
                    # hardcoded k_d = 120
                    differential.append(data["differential"] * 120)
                    setpoint_f.append(data["setpoint_f"])
                    e = data["setpoint_f"] - data["temp_f"]
                    if e > 2:
                        e = 2
                    elif e < -2:
                        e = -2
                    error.append((e))
                    throttle.append(data["throttle"])
                # pylint:disable=all
                # https://matplotlib.org/gallery/subplots_axes_and_figures/subplot.html
                f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
                ax1.set_title('Crock Pot temperatures over time (measurements')

                ax1.set_xlabel('measurements')
                ax1.set_ylabel('temperature in Fahrenheit mostly')

                ax1.plot(x_time, temp_f, 'b', label="temp in F")
                # , marker='o')
                ax1.plot(x_time, setpoint_f, 'k', label='Target Temp')
                ax1.legend()

                ax2.plot(x_time, error, 'r', label='Error', linestyle='--')
                ax2.plot(x_time, integral, 'y', label='Integral')
                ax2.plot(x_time, differential, 'k', label='Differential')
                ax2.plot(x_time, throttle, 'g', label='Throttle')
                ax2.legend()
                # https: // stackoverflow.com/questions/25689238/show-origin-axis-x-y-in-matplotlib-plot
                ax2.axhline(y=1, color='b', linestyle=':')
                ax2.axhline(y=0, color='k')
                ax2.axhline(y=-1, color='b', linestyle=':')
                plt.show(block=True)
                # block=True only needed if
                # plt.ion()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
