import logging

from arhuaco.response.action import Action
# Import the email modules we'll need
from email.mime.text import MIMEText

# Import smtplib for the actual sending function
import smtplib

class Message(Action):

    def __init__(self):
        self.configuration = None

    def execute_action(self, message):
        msg = MIMEText(message)
        msg['Subject'] = 'Red alert!'
        msg['From'] = "arhuaco@locahost"
        msg['To'] = "kurono@localhost"

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail("arhuaco@localhost", ["kurono@localhost"], msg.as_string())
        s.quit()
