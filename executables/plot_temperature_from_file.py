#! /usr/local/bin/env python3

import argparse
import matplotlib.pyplot as plt

import temperature.temperature_file_tools

plt.ion()


def clip_data(y, clip_range):
    if y < clip_range[0]:
        return clip_range[0]
    if y > clip_range[1]:
        return clip_range[1]
    return y


parser = argparse.ArgumentParser(
    description='Plot temperature data written by the temperature controller class')
parser.add_argument('filename',
                    help='required filename (including the path)',
                    type=open)

parser.add_argument('--show-once', '-s', '-1',
                    help='show the plot once and terminate program. Do not re plot after closing the plot window',
                    action="store_true")
parser.add_argument('--max-window', '-m',
                    help='maximize the plot window on opening',
                    action="store_true")

show_only_group = parser.add_mutually_exclusive_group()
show_only_group.add_argument('--temp-only', '-t',  # turned into temp_only with an underscore
                             help='display temperature plot only. (default: show pid plot as well)',
                             action="store_true")
show_only_group.add_argument('--pid-only', '-p',  # turned into pid_only with an underscore
                             help='only show the pid, throttle and error graph',
                             action="store_true")

parser.add_argument('--clip-value', '-c',
                    help='enter the maximum float value (both max and min) for the pid graph',
                    type=float, default=2)
parser.add_argument('--y-limit', '-y',
                    help='set pid y axis at fixed limit (float, both positive and negative',
                    type=float,
                    default=0)
parser.add_argument('--kpid', '-k',
                    help='display the k_p, k_i and k_d values TODO not implemented yet',
                    action="store_true")
parser.add_argument('--interval', '-i',
                    help='display the interval and min_switch_time values TODO not implemented yet',
                    action="store_true")
args = parser.parse_args()
# great "throw parse error" example:
# if args.clip_value < args.y_limit:
#     parser.error(
#         "--clip-value can't be less than --y-limit")

try:
    keep_plotting = True
    while keep_plotting:
        try:
            generator_of_dicts = temperature.temperature_file_tools.read_temperature_control_data_from_file_pickle_generator(
                args.filename.name)
        except:
            print("Issue opening, reading or parsing the file {}".format(
                args.filename.name))
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
                clip_range = (-args.clip_value, args.clip_value)
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
            if args.temp_only:
                f, ax1 = plt.subplots(1, 1)
            elif args.pid_only:  # ignore when both temp_only and pid_only are set...
                f, ax2 = plt.subplots(1, 1)
            else:
                f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

            if not args.pid_only or args.temp_only:  # if both: show temp_only
                ax1.set_title('Crock Pot temperatures over time (measurements')

                ax1.set_xlabel('measurements')
                ax1.set_ylabel('temperature in Fahrenheit mostly')

                ax1.plot(x_time, temp_f, 'b', label="temp in F")
                # , marker='o')
                ax1.plot(x_time, setpoint_f, 'k', label='Target Temp')
                ax1.legend()

            if not args.temp_only:
                ax2.plot(x_time, error, 'r', label='Error', linestyle='--')
                ax2.plot(x_time, integral, 'y', label='Integral')
                ax2.plot(x_time, differential, 'k', label='Differential')
                ax2.plot(x_time, throttle, 'g', label='Throttle')
                ax2.legend()
                # https: // stackoverflow.com/questions/25689238/show-origin-axis-x-y-in-matplotlib-plot
                ax2.axhline(y=1, color='b', linestyle=':')
                ax2.axhline(y=0, color='k')
                ax2.axhline(y=-1, color='b', linestyle=':')
                if args.y_limit != 0:
                    ax2.set_ylim(-args.y_limit, args.y_limit)

            if args.kpid:
                pass

            if args.interval:
                pass

            # if args.min_max_i:  # does not exist yet
            #     pass

            # if args.min_max_throttle:  # does not exist yet
            #     # This is pretty obvious though
            #     pass

            if args.max_window:
                # https: // stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python/18824814  # 18824814
                mng = plt.get_current_fig_manager()
                mng.resize(*mng.window.maxsize())

            plt.show(block=True)
            # block=True only needed if
            # plt.ion()
            keep_plotting = not args.show_once

except KeyboardInterrupt:
    print("KeyboardInterrupt")
