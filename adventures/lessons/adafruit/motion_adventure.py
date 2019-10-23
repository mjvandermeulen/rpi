# pylint: skip-file

import time
import board
import digitalio

# set up motion sensor
pir_sensor = digitalio.DigitalInOut(board.D24)
pir_sensor.direction = digitalio.Direction.INPUT

# set up door sensor
door_sensor = digitalio.DigitalInOut(board.D23)
door_sensor.direction = digitalio.Direction.INPUT

d = 0

while True:

    # if pir_sensor.value:
    #     print("PIR ALARM!")

    if door_sensor.value:
        d += 1
        print("DOOR ALARM! {:3d}".format(d))

    time.sleep(0.5)
