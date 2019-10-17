#!/usr/local/bin/env python3

import tools.mail.automation_email

tools.mail.automation_email.send_family_sms(
    ['Maarten'], 'Test Subject', 'Test Body', True)
