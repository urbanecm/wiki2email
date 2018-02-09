#!/usr/bin/env python
#-*- coding: utf-8 -*-

import yaml
config = yaml.load(open('config.yaml'))
from wmflabs import db
conn = db.connect(config['DB_NAME'])
import sys
import os
import cgi

if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		confirmcode = qs['confirmcode'][0]
	except:
		print 'Bad request'
		sys.exit()
else:
	print 'Bad request'
	sys.exit()

with conn.cursor() as cur:
	sql = 'select email from users where confirmcode=?'
	cur.execute(sql, (confirmcode,))
	data = cur.fetchall()
	if len(data) != 1:
		print 'Bad request'
		sys.exit()

email = data[0][0]

with conn.cursor() as cur:
	sql = 'update users set confirmed=1 where email=?'
	cur.execute(sql, (email, ))

print 'Location: /wiki2email'
print
