#!/usr/local/bin/env python3

import re
import time
import smtplib


# TODO keep this or change to personal_settings
from settings import personal_settings as personal


def send_email_smtp_gmail(user, pwd, recipients, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    gmail_from = user
    gmail_to = recipients if isinstance(recipients, list) else [recipients]
    gmail_subject = subject
    gmail_body = body

    # Prepare actual message
    message = "From: %s\nTo: %s\nSubject: %s\n\n%s" \
        % (gmail_from, ", ".join(gmail_to), gmail_subject, gmail_body)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_from, gmail_to, message)
        server.close()
    except:
        print("Failed to send email")


def send_gmail_email(recipients, subject, body, addtime=False):
    user = personal.gmail_account['user']
    pwd = personal.gmail_account['app_password']

    if not subject:
        subject = 'RPi'

    if addtime:
        body = time.strftime('%a, %b %m %I:%M:%S%p') + '\n' + body
    send_email_smtp_gmail(user, pwd, recipients, subject, body)


def contains_phone_number(email_address):
    p = re.compile(
        r"""
            \d{9,}  # nine or more digits in a row
        """,
        re.IGNORECASE | re.VERBOSE
    )
    return bool(p.search(email_address))


def send_family_message_by_methods(names, methods, subject, body, addtime=False):
    """
    see method options in personal_settings.py (sms or email)

    Parameters
    ----------
    names : list or string
        family member's name(s)
    methods : string
        email or sms
    subject : string
        subject
    body : string
        body
    addtime : bool, optional
        Add a human readable timestamp to the message (the default is False, which does not add the time to the message)
    """

    if not type(names) is list:
        names = [names]  # has to be a list
    for name in names:
        recipients = []
        name = name.lower()  # has to be lower case
        if name in personal.family_addresses:
            if not type(methods) is list:
                methods = [methods]  # has to be list
            # used to be ternary like:
            #     methods = methods if type(methods) is list else [methods]
            for method in methods:
                recipients.append(personal.family_addresses[name][method])
            send_gmail_email(recipients, subject, body, addtime)
        else:
            print(name + ' not in personal.family_addresses dictionary.' + __file__)


# cleanest way to call send_family_sms with time is
# e.g.: send_family_sms('Maarten', '', 'I am doing fine', addtime=True)
def send_family_sms(names, subject, body, addtime=False):
    send_family_message_by_methods(names, ['sms'], subject, body, addtime)


def send_family_email(names, subject, body, addtime=False):
    send_family_message_by_methods(names, ['email'], subject, body, addtime)


def send_family_email_and_sms(names, subject, body, addtime=False):
    send_family_message_by_methods(
        names, ['sms', 'email'], subject, body, addtime)


def list_of_safe_senders_substrings():
    """
    Not sure where this will be needed

    Returns
    -------
    list of string
        list of email addresses without the @... part
    """

    safe_list = []
    for name in personal.family_addresses:
        # check if exists you can loop over the dictonary and test for sms or email
        # turn into (not very legible list comprehension)??? since you're just creating a list with a condition.
        #   NOPE: You're not looping over a list, but over a dictionary (multiple levels)
        safe_list.append(name['sms'].split('@')[0])
        safe_list.append(name['email'].split('@')[0])
    return safe_list
