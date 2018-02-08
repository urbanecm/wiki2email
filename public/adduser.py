#!/usr/bin/env python
#-*- coding: utf-8 -*-

import yaml
config = yaml.load(open('config.yaml'))
from wmflabs import db
conn = db.connect(config['DB_NAME'])
import sys
import os
import cgi
import cgitb
from email.mime.text import MIMEText
import smtplib
import random
import hashlib

if os.environ['REQUEST_METHOD'] != 'POST':
	print 'Use POST please'
	sys.exit()

form = cgi.FieldStorage()
mail = form.getvalue('email')
base = mail + str(random.randint(0, 1000))
m = hashlib.md5()
m.update(base)
confirmhash = m.hexdigest()

with conn.cursor() as cur:
	sql = 'select * from users where email=?'
	cur.execute(sql, (mail))
	data = cur.fetchall()
	if data != 0:
		print 'Exists'
		sys.exit()

with conn.cursor() as cur:
	sql = 'insert into users(email, confirmcode) values (? ,?)'
	cur.execute(sql, (mail, confirmhash))

emailtext = u"""Dobrý den,

někdo, pravděpodobně Vy, požádal o zařazení e-mailové adresy %s do mailové služby na pravidelné zasílání článků z Wikipedie do e-mailu. Prosíme o potvrzení kliknutím na následující odkaz.

Potvrzení: %s

--
Váš zasílač wiki článků do e-mailu

Kontakt: martin.urbanec@wikimedia.cz
""" % (mail, "https://tools.wmflabs.org/wiki2email/confirmmail.py?email=" + mail + '&confirm=' + confirmhash)

we = 'urbanecm@tools.wmflabs.org'
s = smtplib.SMTP('mail.tools.wmflabs.org')
msg = MIMEText(emailtext.encode('utf-8'))
msg['Subject'] = 'Potvrzení e-mailové adresy'
msg['From'] = we
msg['To'] = mail
s.sendmail(we, mail, msg.as_string())
s.quit()
