#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Import libs
import yaml
config = yaml.load(open('/data/project/wiki2email/wiki2email/public/config.yaml'))
from wmflabs import db
conn = db.connect(config['DB_NAME'])
import datetime
import pywikibot
import smtplib
import mwparserfromhell
import requests
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from WikiToPlain import Wiki2Plain

# Config libs
site = pywikibot.Site()

# Fix encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Fetch article from Wikipedia

yearweek = datetime.date.today().isocalendar()[:2]
title = 'Wikipedie:Článek týdne/%04d/%02d' % yearweek
page = pywikibot.Page(site, title)
code = mwparserfromhell.parse(page.text)
for template in code.filter_templates():
	if template.name.strip().lower() == u'čt':
		for param in template.params:
			if param.name.strip() == u'název':
				article = param.value.strip()
				break
		break

# Fetch the article's first paragraph
page = pywikibot.Page(site, article)
text = str(Wiki2Plain(page.text)).split('\n\n')[0]

# Prepare mails

emailtext = """Článek týdne: %s

%s

Plný text: %s

--
Váš zasílač článků týdne

Kontakt: martin.urbanec@wikimedia.cz
""" % (article, text, "https://cs.wikipedia.org/wiki/" + article.replace(' ', '_'))


# Fetch emails
emails = []
with conn.cursor() as cur:
	sql = 'select email from users where confirmed=1'
	cur.execute(sql)
	data = cur.fetchall()
for line in data:
	emails.append(line[0])

# Send mails!!!
we = 'urbanecm@tools.wmflabs.org'
s = smtplib.SMTP('mail.tools.wmflabs.org')
for email in emails:
	msg = MIMEText(emailtext.encode('utf-8'))
	d = datetime.datetime.today()
	msg['Subject'] = '%s. %s. %s: %s' % (d.day, d.month, d.year, article)
	msg['From'] = we
	msg['To'] = email
	s.sendmail(we, email, msg.as_string())
s.quit()
