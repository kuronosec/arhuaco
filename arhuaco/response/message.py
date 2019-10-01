# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import logging

from arhuaco.response.action import Action
from email.mime.text import MIMEText

import smtplib

# Sends an alert message to the administrators

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
