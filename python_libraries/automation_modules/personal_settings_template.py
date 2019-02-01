#!/usr/local/bin/env python3
# TEMPLATE ONLY
# THESE NOTES APPLY TO personal_settings.py ONLY!
# When it comes to RF Outlets the only private info is the codes in this file
# NOTE: all "off codes" are "on code" + 9
# https://timleland.com/wireless-power-outlets/
# See README.txt in the rfo folder (remote_frequency_outlets) # Check TODO
# END TEMPLATE ONLY


# COPY TO personal_settings.py
# this file is in .gitignore
# WHEN MAKING CHANGES MAKE SURE THE file personal_setting_template.py is updated as well
# For more notes see that file.
# Notes in here are personal, or related to personal values.

family_addresses = {
    'name1': {
        'sms': 'xxxxxxxxxx@messaging.sprintpcs.com',
        'email': 'xxx@xxx.xxx',
        'prefer_sms_reply': True,
    },
    'name2': {
        'sms': 'xxxxxxxxxx@messaging.sprintpcs.com',
        'email': 'xxx@xxx.xxx',
        'prefer_sms_reply': False,
    },
}

gmail_account = {
    'user': 'some_name@gmail.com',  # @todo try without @gmail.com
    'app_password': 'xxxxxxx',
}

rfoutlet_codes = {
    '1': {
        'on': 1234567,
        'off': 1234567,
    },
    '2': {
        'on': 1234567,
        'off': 1234567,
    },
    '3': {
        'on': 1234567,
        'off': 1234567,
    },
    '4': {
        'on': 1234567,
        'off': 1234567,
    },
    '5': {
        'on': 1234567,
        'off': 1234567,
    },
}
