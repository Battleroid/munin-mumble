#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request, abort, g
import sqlite3 as sql
DATABASE = 'idle.db'
app = Flask(__name__)

# SQL & DB 
def connect_db():
	return sql.connect(DATABASE)

def grab_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = connect_db()
	return db

@app.teardown_appcontext
def close_db(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
	cur = grab_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

# ERROR HANDLING
@app.errorhandler(404)
def page_not_found(e):
	return render_template('error/404.html', error=e), 404

# API
@app.route('/api/', methods=['GET'])
def all_users():
	data = query_db('select * from users order by points desc')
	if data is None:
		return jsonify({})
	users = []
	total = 0
	for user in data:
		users.append({'name': user[0], 'points': user[1]})
		total = total + user[1]
	return jsonify(users=users, total=total, registered=len(data))

@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
	data = query_db('select name, points from users where name = ?', (username, ), True)
	if data is None:
		return jsonify({})
	return jsonify({'name': data[0], 'points': data[1]})

# ROUTING
@app.route('/')
def default():
	data = query_db('select * from users order by points desc')
	last = data[-1][0]
	reg = len(data)
	time = 0
	for user in data:
		time += user[1]
	return render_template('leaderboard.html', data=(data, reg, time, last))

if __name__ == '__main__':
	app.run(host='0.0.0.0')
