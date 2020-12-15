# Crockpot

crockpot.py needs to be changed to cooking thermostat / thermostat or whatever.

To execute:

    pi@raspberrypi:~/Programming/Automation/executables $  python3 crockpot.py

# Plotting

in the directory with the data:

    pi@raspberrypi:~/Programming/Automation/measurements/temperature_controller $ python3 ../../executables/plot_temperature_from_file.py --max-window warm-compress-2020-12-10_16-43.pickle

recommendation: first run with --help

the replotting only occurs after closing the window and it's a little finicky to close the window permanently. See --help for 1 time showing of graph.
