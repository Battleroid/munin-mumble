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
	''' Return all users and other metrics. '''
	data = query_db('select * from users order by points desc')
	if data is None:
		return jsonify({})
	total = query_db('select sum(points) from users', (), True)[0]
	return jsonify(users=data, metrics={'registered': len(data), 'total_time': total})

@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
	''' Return the information for a single user. '''
	data = query_db('select * from users where name = ?', (username, ), True)
	if data is None:
		return jsonify({})
	return jsonify(user={'name': data[0], 'points': data[1]})

# ROUTING
@app.route('/')
def default():
	data = query_db('select * from users order by points desc')
	time = query_db('select sum(points) from users', (), True)[0]
	last = data[-1][0]
	reg = len(data)
	return render_template('leaderboard.html', data=(data, reg, time, last))

if __name__ == '__main__':
	app.run(host='0.0.0.0')
