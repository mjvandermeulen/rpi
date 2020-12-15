#!/usr/bin/env python

import subprocess
import re
import time
import math

from settings import automation_settings

# Transmitter module
# DATA (left pin) -> GPIO #17
# VCC (center pin) -> +5VDC
# GND (right pin) -> Ground
#
# Receiver Module
# VCC (left pin) -> +5VDC
# DATA (2nd pin from left) -> GPIO 21/27
# GND (far right pin) -> Ground

# @todo move some of these to automation_settings.
# AUTOMATION_EXECUTABLES_PATH = '/home/pi/Programs/subprocesses/'  # end with '/'
RFOUTLET_DIR = '/home/pi/rfoutlet/'  # end with '/'
CODESEND_COMMAND = 'codesend'
PULSELENGTH = automation_settings.rfpulse_length  # TODO cleanup
OUTLET_CODES = automation_settings.rfoutlet_codes

MONTH_DICT = {
    'jan': '01',
    'feb': '02',
    'mar': '03',
    'apr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dec': '12',
}


# return string group
# '' if no such group
def parse_proper_outlet_group_name(group):
    group = group.lower()
    for key in automation_settings.outlet_groups:
        p = re.compile(
            automation_settings.outlet_groups[key].regex + '$', re.X | re.I)
        if p.match(group):
            return key
    return ''


def send_code(code):
    """
    Use default pin = 0
    see wiring pi: http://wiringpi.com/pins/
    0 --> BCM 17 (not the GPIO 1.. {x @todo} numbering)
    """
    subprocess.call([
        'sudo',
        RFOUTLET_DIR + CODESEND_COMMAND,
        str(code),
        '-l',
        PULSELENGTH
    ])


##
# @brief      turns outlets in list on or off.
##
# @param      group  list of outlets e.g.: ['1', '3']
# @param      on     { parameter_description }
##
# @return     None @todo: return True or error message.
# First check if outlets in OUTLET_CODES
##
# improvement @todo @maarten:
# move attempts to python program (sub process)
# called by send_code
# todo: check if group exists.
def switch_outlet(outlets, mode="off", attempts=1, delay=1):

    for i in range(attempts):
        if i > 0:
            time.sleep(delay/2)  # ***** TODO HACK: allow float!!!!
        for outlet in outlets:
            # print 'sending code for outlet: ' + outlet + ' with mode: ' + mode
            # print OUTLET_CODES[outlet][mode]
            # print
            send_code(OUTLET_CODES[outlet][mode])


def blink_outlet(outlets, mode='blink', blink=(0, 0, 0)):
    # refer to settings for default blinks here and here only TODO
    blinks = blink[0] if not blink[0] is None else 5
    blinkon = blink[1] if not blink[1] is None else 1
    blinkoff = blink[2] if not blink[2] is None else 1

    for i in range(blinks):
        if i > 0:
            time.sleep(blinkoff)
        for outlet in outlets:
            send_code(OUTLET_CODES[outlet]['on'])
        time.sleep(blinkon)
        if not(i + 1 == blinks and (mode == 'n' or mode == 'on')):
            for outlet in outlets:
                send_code(OUTLET_CODES[outlet]['off'])


def switch_outlet_group(outlet_group, mode="off", attempts=3, delay=1, blink=(0, 0, 0)):
    outlets = []
    # Check if outlet_group given is already a key in automation_settings.outlet_groups (already properly named)
    if outlet_group in automation_settings.outlet_groups.keys():
        outlets = automation_settings.outlet_groups[outlet_group].outlets
    else:
        for key in automation_settings.outlet_groups:
            p = re.compile(
                automation_settings.outlet_groups[key].regex, re.X | re.I)
            if p.match(outlet_group):
                outlet_group = key
                outlets = automation_settings.outlet_groups[key].outlets
                break  # outlet group match found
    if len(outlets) == 0:
        return 'No outlets switched, probably because the group does not exist...'
        # Maarten doesn't think it should be
        # possible to get here.
        # A group would need to have an empty outlets list
        # Wrong: executables/rfoutlets_switch_group.py calls this from the commandline
        # The groups are not checked here.

    if attempts is None:
        attempts = 3  # TODO settings
    if delay is None:
        delay = 1  # TODO settings

    if mode == 'blink' or (not blink[0] is None and blink[0] > 0):
        blink_outlet(outlets, mode, blink)
    else:
        if 'n' in mode:
            mode = 'on'
        else:
            mode = 'off'
        switch_outlet(outlets, mode, attempts)

    if outlet_group.isnumeric():
        r = "Outlet "
    else:
        r = "Outlet group "

    return r + outlet_group + " turned " + mode + "."


def rfo_schedule_in_minutes(group, mode, minutes_from_now, attempts=3, delay=1, blink=(0, 0, 0)):
    time_string = 'now + {} minute'.format(int(math.ceil(minutes_from_now)))
    rfo_schedule(time_string, group, mode, minutes_from_now,
                 attempts, delay, blink)


def rfo_schedule(time_string, group, mode, minutes_from_now, attempts=3, delay=1, blink=(0, 0, 0)):
    print("timestring " + time_string)
    sched_cmd = ['at', time_string]
    args = ''
    if attempts != 3:
        args += ' --attempts {}'.format(attempts)
    if delay != 1:
        args += ' --delay {}'.format(delay)
    if blink[0] != 0:
        args += ' --blinks {}'.format(blink[0])
    if blink[1] != 0:
        args += ' --blinkon {}'.format(blink[1])
    if blink[2] != 0:
        args += ' --blinkoff {}'.format(blink[2])
    command = 'python3 {}rfoutlets_switch_group.py {} {} {}'.format(
        automation_settings.AUTOMATION_EXECUTABLES_PATH, group, mode, args)
    print
    print(command)
    p = subprocess.Popen(sched_cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate(command)
    print
    print("output rfo_schedule at linux")
    print(output)
    print("end output rfo_schedule at linux")


# # returns tupel (string, string)
# #               (time,   job)
# # error:        ('',     '')
# def parse_at_scheduler_time_and_job(output):
#     pattern_string = r"""
#         job
#         \s*           # whitespace
#         (?P<job>\d*)  # job number: Capture these digits in named group 'job'
#         \s*
#         at
#         \s*
#         (?P<time>.+)  # time: Capture in named group 'time'
#         $
#     """
#     p = re.compile(pattern_string, re.VERBOSE | re.IGNORECASE | re.MULTILINE)
#     matchObj = p.search(output)
#     if matchObj:
#         return matchObj.group('time'), matchObj.group('job')
#     else:
#         return '', ''


# # return tupel (message, job, time)
# #              (string, string, string)
# #              (either error or time, either '' in case of error or job number, time or '')
# def switch_outlet_group_at(group, mode, time):
#     sched_cmd = ['at', time]
#     command = 'python {}rfoutlets_switch_group.py {} {}'.format(
#         AUTOMATION_EXECUTABLES_PATH, group, mode)
#     p = subprocess.Popen(sched_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output = p.communicate(command)[1]  # includes warning
#                                         # e.g.:
#                                         # 'warning: commands will be executed using /bin/sh\njob 21 at Thu Aug 25 14:39:00 2016\n'
#     print output
#     time, job = parse_at_scheduler_time_and_job(output)
#     if job != '':
#         message = 'Turning group {} {} {}. (Job: {})'.format(
#             group,
#             mode,
#             time,
#             job
#         )
#         return message, job, time
#     elif 'garble' in output.lower():
#         # @todo: give correct examples.
#         return 'Incorrect time given', '', ''

#     return 'Error scheduling task', '', ''
