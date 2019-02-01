#!/usr/local/bin/env python3

from automation_modules import automation_email

automation_email.send_family_sms(
    ['Maarten'], 'Test Subject', 'Test Body', True)
