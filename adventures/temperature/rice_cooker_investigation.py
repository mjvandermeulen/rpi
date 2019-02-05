import time

from automation_classes import temperature
from automation_classes import powertail
from automation_modules import automation_email

interval = 30  # seconds
# Just to make sure the powertail is not switching after just one second... NEEDED?
min_switch_time = 2

temp_profile = [
    # (k_p, time in seconds)
    (0.005, 1 * 3600),
    (0.01,  1 * 3600),
    (0.02,  3/4 * 3600),
    (0.05,  1/2 * 3600),
    (0.1,   1/2 * 3600),
    (0.5,   1/2 * 3600)
]


temp = temperature.Temperature(0, interval, 'test-after-cbd')
power = powertail.PowerTail('BCM', 23, False)


try:
    for section in temp_profile:
        t = start_of_section = time.time()
        while t < start_of_section + section[1]:
            print()
            print("=== start while loop in " + __file__ + " ===")
            print()
            temp.change_setpoint(section[0])
            temp_f = temp.read_temp_f()  # change to name without f (does not matter here)
            if temp_f > section[0]:
                temp.send_temp_reached_notification(
                    section[0], 'maarten', 4, 1)

            throttle = temp.throttle

            # power control
            power.run_throttled_power_interval(
                power, throttle, -1, +1, interval, min_switch_time)
            print()
            print("=== end while loop in " + __file__ + " ===")
            print()
            t = time.time()

except KeyboardInterrupt:
    print("keyboard interrupt")
    power.turn_off()
    temp.detach_plot()
    # program halts here
