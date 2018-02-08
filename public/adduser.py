#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import cgi
import cgitb
from email.mime.text import MIMEText
import smtplib

if os.environ['REQUEST_METHOD'] != 'POST':
	print 'Use POST please'
	sys.exit()

form = cgi.FieldStorage()
mail = form.getvalue('email')

emailtext = u"""Dobrý den,

někdo, pravděpodobně Vy, požádal o zařazení e-mailové adresy %s do mailové služby na pravidelné zasílání článků z Wikipedie do e-mailu. Prosíme o potvrzení kliknutím na následující odkaz.

Potvrzení: %s

--
Váš zasílač wiki článků do e-mailu

Kontakt: martin.urbanec@wikimedia.cz
""" % (mail, "https://tools.wmflabs.org/wiki2email/confirmmail.py?email=" + mail)

we = 'urbanecm@tools.wmflabs.org'
s = smtplib.SMTP('mail.tools.wmflabs.org')
msg = MIMEText(emailtext.encode('utf-8'))
msg['Subject'] = 'Potvrzení e-mailové adresy'
msg['From'] = we
msg['To'] = email
