#!/usr/local/bin/env python3

import collections
from settings import personal_settings

AUTOMATION_PROJECT_PATH = '/home/pi/Programming/Automation/'  # end with '/'
TEMPCONTROLLER_MEASUREMENTS_PATH = AUTOMATION_PROJECT_PATH + \
    'measurements/temperature_controller/'
AUTOMATION_EXECUTABLES_PATH = AUTOMATION_PROJECT_PATH + \
    'executables/'

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
    # pytest only:
    '1000': OutletGroup(
        r'10|tho?u?sa?nd?',
        ['1000'],
    ),

    'livingroom': OutletGroup(
        r'l(?:iving)?r(?:oom)?s?',
        ['1', '2', '3'],
    ),

    # '"fans (noise)"': OutletGroup(
    #     r'noise?s?|fans',
    #     ['7', '3'],
    # ),
    'tree': OutletGroup(
        r'tre?e?s?',
        ['4'],
    ),
    # 'snowman': OutletGroup(
    #     r'sno?wm?a?n?',
    #     ['6'],
    # ),
    'coffee': OutletGroup(
        r'co?ff?e?e?',
        ['6'],
    ),
    'airfilter': OutletGroup(
        r'(air)?[ ]?(fi?lte?r|pu?ri?fi?e?r)',
        ['7'],
    ),
    'fan': OutletGroup(
        r'fan\b',  # not fans: see regex with fans.
                   # so word boundary needed.
                   # word boundary overlaps with next wordboundary
                   # see debuggex.com, but no problem because
                   # r'fan\b\b\b\b\b' works equally well.
        ['8'],
    ),
    'dehumidifier': OutletGroup(
        r'de?hu?i?d?i?f?i?e?r?',
        ['9']
    ),
    'officenoise': OutletGroup(
        r'o?ff?i?ce?no?i?s?e?',
        ['8', '9']
    ),
    'basement': OutletGroup(
        # 'b(ase)?m(ment)?s?',
        # no (?:...) non-capturing groups needed, since only named groups
        # are used
        r'ba?s?e?me?n?t?s?',  # yields 2^7 possibilities...
        ['10'],
    ),
    # 'humidifier': OutletGroup(
    #     r'hu?mi?d(ifier)?s?',
    #     ['7'],
    # ),
    # 'cooler': OutletGroup(
    #     r'co?o?le?r?',
    #     ['6'],
    # ),
    # 'red-light': OutletGroup(
    #     r're?d([ ]?lights?)?',
    #     ['4'],
    #     ),
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

Brew_Settings = collections.namedtuple(
    'Brew_Settings', 'cycles brew_time pause')
coffee_settings = {
    "default": Brew_Settings(2, 15*60, 15*60),
    "clean": Brew_Settings(30, 20, 15*60),
    "rinse": Brew_Settings(1, 3*60, 10*60),
    "test": Brew_Settings(1, 1, 10)
}
coffee_default_delay = 0
