# create a class
# usage:
#  create an instance, with addressee
#  method:
#      check if mail needs to be sent depending on current AND PAST temperature!

from automation_modules import automation_email


def send_temp_reached_notification(self, temp, name, number_of_readings, step=1):
    """
    TODO mail number_of_readings readings (with step)
    """

    subject = 'Reached {} F'.format(temp)
    body = "Current Temp: {}\n\n".format(self.current_temp_f) + \
        "TODO throttle (control function = u)"

    automation_email.send_family_email_and_sms(
        name, subject, body, addtime=True)
