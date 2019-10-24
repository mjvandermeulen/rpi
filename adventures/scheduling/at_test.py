#!/usr/bin/env python

import subprocess
import re

RFOUTLET_PYTHON_DIR = '/home/pi/Programming/Automation/executables/'  # end with '/'

# http://stackoverflow.com/a/10676359

# sudo apt-get update
# sudo apt-get install at


def at_test():
    group = '2'
    mode = 'on'
    time = 'now + 1 minute'
    sched_cmd = ['at', time]
    print(sched_cmd)
    command = 'python {}rfoutlets_switch_group.py {} {}'.format(
        RFOUTLET_PYTHON_DIR, group, mode)
    print(command)
    p = subprocess.Popen(sched_cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate(command)
    print("output")
    print(output)
    print("end output")


def atq_test():
    sched_cmd = ['atq']
    p = subprocess.Popen(sched_cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()
    print("output")
    print(output)
    print("end output")


def atrm_test(n):
    sched_cmd = ['atrm', n]
    p = subprocess.Popen(sched_cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()
    print("output")
    print(output)
    print("end output")


def atrm_all_test():
    # http://unix.stackexchange.com/a/53148
    # output = subprocess.check_output to check output
    subprocess.call(
        "for i in `atq | awk '{print $1}'`;do atrm $i;done", shell=True)


def jobs_from_atq():
    atq_out = subprocess.check_output(['atq'])  # atq is alias of "at -l"
    print(atq_out)
    pattern_string = r"""
        ^   # beginning of line
        (?P<job>
            \d+
        )
        .* # anything lazy
        $   # end of line. (re.MULTILINE NEEDED)
    """
    p = re.compile(pattern_string, re.X | re.M)  # re.M is important here
    job_numbers = p.findall(atq_out)
    print(job_numbers)
    return job_numbers


def remove_all_at_jobs():
    jobs = jobs_from_atq()
    for job in jobs:
        subprocess.call(['atrm', job])


def remove_at_job(job):
    try:
        subprocess.call(['atrm', job])
    except TypeError:
        print("job not of correct type string")


# remove_at_job('32')
# at_test()
# atq_test()
# atrm_test('1')
# atrm_all_test()
# remove_all_at_jobs()
