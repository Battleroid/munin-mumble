#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request, abort, g
import sqlite3 as sql
DATABASE = 'idle.db'
app = Flask(__name__)

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

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error/404.html', error=e), 404

@app.route('/user', methods=['GET'])
def all_users():
	data = query_db('select * from users order by points desc')
	if data is None:
		return 'No users available.'
	users = []
	for user in data:
		users.append({'name': user[0], 'points': user[1]})
	return jsonify(users=users)

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
	data = query_db('select * from users where name = ?', (username, ), True)
	if data is None:
		abort(404)
	user = {'name': data[0], 'points': data[1]}
	return jsonify(user=user)

@app.route('/')
def default():
	data = query_db('select * from users order by points desc')
	return render_template('leaderboard.html', data=data)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
