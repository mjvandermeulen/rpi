BOARD = 1
OUT = 1
IN = 1

BCM = True


def setmode(a):
    print("mac_dummy_libraries: RPi.GPIO. Parameter: {}".format(a))


def setup(a, b):
    print("mac_dummy_libraries: RPi.GPIO. Parameter: {}".format(a))


def input(a):
    print("mac_dummy_libraries: RPi.GPIO. Parameter: {}".format(a))


def output(a, b):
    print("mac_dummy_libraries: RPi.GPIO. Parameter: {}".format(a))


def cleanup():
    print("mac_dummy_libraries: RPi.GPIO.")


def setwarnings(flag):
    print("mac_dummy_libraries: RPi.GPIO. Parameter: {}".format(flag))
