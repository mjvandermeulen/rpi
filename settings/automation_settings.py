#!/usr/local/bin/env python3

import collections
from settings import personal_settings

automation_project_path = '/home/pi/Programming/Automation'
tempcontroller_measurements_path = automation_project_path + \
    '/measurements/temperature_controller'

### remote frequency outlets ###
################################

rfoutlet_codes = personal_settings.rfoutlet_codes
# pulse length 195 average
rfpulse_length = '195'

# includes homophones (specific form of homonym): '4', 'four', 'for', 'fore'
# NOTE every outlet command is a group, including 1..5
# @todo replace string with r'...'
# @todo: change name to rfoutlet_groups
# @todo: hierarchy noise points to fan and filter? -> you need to recursively
#   find the base groups.
#
# NOTE: no spaces in the keys OR key: '"fans (noise)"' --> wrap in double quotes
#         so the key is actually contains the double quotes: "fans (noise)"

# Fluent Python implemented
OutletGroup = collections.namedtuple('OutletGroup', ['regex', 'outlets'])

outlet_groups = {
    '1': OutletGroup(
        r'1|one|won',  # '1|w?one?' adds incorrect on: problem!
        ['1'],
    ),
    '2': OutletGroup(
        r'2|t[wo]?o',
        ['2'],
    ),
    '3': OutletGroup(
        r'3|three',
        ['3'],
    ),
    '4': OutletGroup(
        r'4|fou?re?',  # adds incorrect foure. no problem :)
        ['4'],
    ),
    '5': OutletGroup(
        r'5|five',
        ['5'],
    ),
    '6': OutletGroup(
        r'6|six|st?icks?',
        ['6'],
    ),
    '7': OutletGroup(
        r'7|seven',
        ['7'],
    ),
    '8': OutletGroup(
        r'8|eight|h?ate',
        ['8'],
    ),
    '9': OutletGroup(
        r'9|nine|nein',
        ['9'],
    ),
    '10': OutletGroup(
        r'10|t[aei]e?n',
        ['10'],
    ),
    'coffee': OutletGroup(
        r'co?ff?e?e?',
        ['1'],
    ),
    'airfilter': OutletGroup(
        r'(air)?[ ]?(fi?lte?r|pu?ri?fi?e?r)',
        ['2'],
    ),
    'fan': OutletGroup(
        r'fan\b',  # not fans: see regex with fans.
                   # so word boundary needed.
                   # word boundary overlaps with next wordboundary
                   # see debuggex.com, but no problem because
                   # r'fan\b\b\b\b\b' works equally well.
        ['3'],
    ),
    '"fans (noise)"': OutletGroup(
        r'noise?s?|fans',
        ['2', '3'],
    ),
    'tree': OutletGroup(
        r'tre?e?s?',
        ['4', '5'],
    ),
    'snowman': OutletGroup(
        r'sno?wm?a?n?',
        ['6'],
    ),
    # 'humidifier': OutletGroup(
    #     r'hu?mi?d(ifier)?s?',
    #     ['7'],
    # ),
    # 'basement': OutletGroup(
    #     # 'b(ase)?m(ment)?s?',
    #     # no (?:...) non-capturing groups needed, since only named groups
    #     # are used
    #     r'ba?s?e?me?n?t?s?',  # yields 2^7 possibilities...
    #     ['9', '10'],
    # ),
    # 'cooler': OutletGroup(
    #     r'co?o?le?r?',
    #     ['6'],
    # ),
    # 'red-light': OutletGroup(
    #     r're?d([ ]?lights?)?',
    #     ['4'],
    #     ),
    # 'livingroom': OutletGroup(
    #     'l(?:iving)?r(?:oom)?s?',
    #     ['1', '2'],
    #     ],
    # 'lights': OutletGroup(
    #     r'li?g?h?te?s?',
    #     [],
    # ),
}

# Fluent Python implemented
# declare groups_regex, used in the outlets regex below.
groups_list = [outlet_groups[key].regex for key in outlet_groups]
# groups_list now looks like:
# ['1|one|won', '2|t[wo]?o', ..., 'noise?s?']
groups_regex = '|'.join(groups_list)
# groups_regex now looks like:
# '1|one|won|2|t[wo]?o|...|noise?s?'

### END remote frequency outlets ###
####################################
