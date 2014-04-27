#!/usr/bin/env python
import sqlite3 as sql
import mumble, sys

con = None

try:
	# get
	m = mumble.connect()
	users = []
	data = m.getUsers()
	for key in data.keys():
		if (data[key].userid != -1):
			name = data[key].name.decode('utf-8')
			comment = data[key].comment.decode('utf-8')
			users.append([name, comment])
	# sql
	con = sql.connect(sys.argv[1])
	cur = con.cursor()
	for user in users:
		cur.execute("update users set points = points + 1 where name = ?;", (user[0],))
		cur.execute("update users set comment = ? where name = ?;", (user[1], user[0],))
		cur.execute("insert or ignore into users (name, comment, points) values (?, ?, 1);", (user[0], user[1],))
		cur.execute("update users set date = datetime('now') where name = ?;", (user[0],))
	con.commit()
except sql.Error, e:
	if con:
		con.rollback()
	print 'Error: %s' % e.args[0]
	sys.exit(1)
finally:
	if con:
		con.close()

