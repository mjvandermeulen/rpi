# TODO delete this file
# moved to crockpot.py in executables
#
# # #!/usr/bin/env python3

# import time

# from automation_classes import temperature
# from automation_classes import powertail

# # TODO ##### move to settings profile
# target_temp = 179
# notify_when_setpoint_reached = True
# notify_temps = [175]
# warning_temps = [190]
# # later: system_on_notifications_per_day = 10

# # TODO: move to init or even better: to temp_control_settings.py
# k_p = 0.5

# # integral is error (in F) times time (s). OLD: 0.05 -> 0.0008333333 say 0.0008
# # seems like a good value, not tested yet Jan 28. 0.0005 TEsted and working great. Slight fluctuation, but in bounds.
# k_i = 0.0005

# # differential is measured in Fahrenheit per second (F/s, like velocity in distance over time graph)
# # 120 was working. Now 100, but since only measure one minute back, this is a little much. (still working wonderfully though)
# k_d = 60

# # TODO: think about this value. This only needs to be this high if you cook something just above room temp :) Kombucha?
# min_i = -1 / k_i

# # (full throttle, at level (d == 0) target temperature (p == 0). Tinkering possible here.)
# max_i = 1 / k_i

# min_dx = 60  # to be implemented, still hardcoded

# interval = 60  # seconds
# # Just to make sure the powertail is not switching after just one second... NEEDED?
# min_switch_time = 2

# temp = temperature.Temperature(  # reverse max and min_i
#     target_temp, k_p, k_i, k_d, max_i, min_i, min_dx=min_dx, interval=interval, minimum_switch_time=)

# power = powertail.PowerTail('BCM', 23, False)

# try:

#     while True:
#         print()
#         print("=== start while loop in " + __file__ + " ===")
#         print()
#         temp_f = temp.read_temp_f()

#         throttle = temp.throttle(-1, 1)
#         print("throttle:{:14.8f}".format(throttle))

#         # temp.plot()

#         # power control
#         # hardcoded min_throttle and max_throttle
#         power.run_throttled_power_interval(
#             power, throttle, -1, 1, interval, min_switch_time)
#         print()
#         print("=== end while loop in " + __file__ + " ===")
#         print()

# except KeyboardInterrupt:
#     print("keyboard interrupt")
#     power.turn_off()
#     temp.detach_plot()
#     # program halts here
