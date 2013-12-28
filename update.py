#!/usr/bin/env python
import sqlite3 as sql
import mumble, sys

con = None

try:
	# get
	m = mumble.connect()
	names = []
	data = m.getUsers()
	for key in data.keys():
		if (data[key].userid != -1):
			names.append([data[key].name])
	# sql
	con = sql.connect(sys.argv[1])
	cur = con.cursor()
	cur.executemany("update users set points = points + 1 where name = ?;", names)
	cur.executemany("insert or ignore into users (name, points) values (?, 1);", names)
	cur.executemany("update users set date = datetime('now') where name = ?;", names)
	con.commit()
except sql.Error, e:
	if con:
		con.rollback()
	print 'Error: %s' % e.args[0]
	sys.exit(1)
finally:
	if con:
		con.close()

