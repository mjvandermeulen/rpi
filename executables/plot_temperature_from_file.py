#! /usr/local/bin/env python3

import sys
import matplotlib.pyplot as plt

from automation_modules import temperature_file_tools as temperature_file_tools

plt.ion()


def clip_data(y, clip_range):
    if y < clip_range[0]:
        return clip_range[0]
    if y > clip_range[1]:
        return clip_range[1]
    return y


try:
    data_file = sys.argv[1]
    show_pid_values = False
    show_min_max_i = False
    show_interval = False
    show_min_max_throttle = False
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
                # x axis
                first_time_stamp = 0
                x_time = []

                # measurements
                temp_f = []

                # settings
                setpoint_f = []
                k_p = []
                k_i = []
                k_d = []
                min_i = []
                max_i = []
                d_x = []
                min_throttle = []
                max_throttle = []
                interval = []
                min_switch_time = []
                # calculations
                error = []
                integral = []
                differential = []
                u = []  # value of the control function
                throttle = []

                for data in generator_of_dicts:
                    # unlikely that the first record was the first second in Jan 1 1970 (start of Unix time)
                    if first_time_stamp == 0:
                        first_time_stamp = data["time_stamp"]
                    # x axis in hours since start of profile
                    x_time.append(
                        (data["time_stamp"] - first_time_stamp) / 3600.0)

                    # settings
                    setpoint_f.append(data["setpoint_f"])
                    k_p.append(data["k_p"])
                    k_i.append(data["k_i"])
                    k_d.append(data["k_d"])
                    min_i.append(data["min_i"])
                    max_i.append(data["max_i"])
                    d_x.append(data["d_x"])
                    min_throttle.append(data["min_throttle"])
                    max_throttle.append(data["max_throttle"])
                    interval.append(data["interval"])
                    min_switch_time = ["min_switch_time"]

                    # measurement
                    temp_f.append(data["temp_f"])

                    # calculations
                    clip_range = (-2, 2)  # hardcoded
                    integral.append(
                        clip_data(data["integral"] * data["k_i"], clip_range))
                    # hardcoded k_d = 120
                    differential.append(
                        clip_data(data["differential"] * data["k_d"], clip_range))
                    e = (data["setpoint_f"] - data["temp_f"]) * data["k_p"]
                    error.append(clip_data(e, clip_range))
                    throttle.append(data["throttle"])
                # ylint:disable=all

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

                if show_pid_values:
                    pass

                if show_min_max_i:
                    pass

                if show_interval:
                    pass

                if show_min_max_throttle:
                    # This is pretty obvious though
                    pass

                # https: // stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python/18824814  # 18824814
                mng = plt.get_current_fig_manager()
                mng.resize(*mng.window.maxsize())

                plt.show(block=True)
                # block=True only needed if
                # plt.ion()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
