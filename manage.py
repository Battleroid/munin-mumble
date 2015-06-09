#!/usr/bin/env python
from flask_script import Manager, Command, Option, prompt_bool
from rankings import app

man = Manager(app)

class Cleanup(Command):
    'Cleanup before removal.'

    def run(self):
        import os
        if os.path.exists('ranks.db'):
            os.remove('ranks.db')

class CreateDB(Command):
    'Create DB before starting.'

    def run(self):
        from database import User, db
        db.connect()
        if not User.table_exists():
            User.create_table()

def check_db():
    'Check if DB exists, ask to create, if denied, abort.'
    from database import User
    if not User.table_exists():
        if prompt_bool('Database does not exist, create it now?'):
            User.create_table()
        else:
            from sys import exit
            Cleanup().run()
            print 'Aborting'
            exit(1)

@man.option('--name', '-n', dest='name', help='name of user', required=True)
@man.option('--points', '-p', dest='points', default=0, type=int, help='no. of points to give', required=False)
def adduser(name, points):
    'Add user to leaderboard.'
    check_db()
    from database import User
    if not User.select().where(User.username==name).exists():
        u = User.create(username=name, points=points)
        if u.id:
            print '{} created.'.format(name)
    else:
        print 'User exists, nothing will happen.'

@man.option('--name', '-n', dest='name', help='name of user', required=True)
def deluser(name):
    'Remove user from leaderboard.'
    check_db()
    from database import User
    u = User.get(User.username==name)
    u.delete_instance()

@man.option('--name', '-n', dest='name', help='name of user', required=True)
@man.option('--points', '-p', dest='points', help='no. of points to subtract', required=True, type=int)
def delpoints(name, points):
    'Remove points from user.'
    check_db()
    from database import User
    u = User.get(User.username==name)
    if (u.points - points) < 0:
        u.points = 0
    else:
        u.points -= points
    u.save()

@man.option('--name', '-n', dest='name', help='name of user', required=True)
@man.option('--points', '-p', dest='points', help='no. of points to add', required=True, type=int)
def addpoints(name, points):
    'Add points to user.'
    check_db()
    from database import User
    u = User.get(User.username==name)
    u.points += points
    u.save()

@man.option('--name', '-n', dest='name', help='name of user', required=True)
@man.option('--points', '-p', dest='points', help='set points to value', default=0, type=int)
def setpoints(name, points):
    'Set points (or reset) for user.'
    check_db()
    from database import User
    u = User.get(User.username==name)
    u.points = points if points >= 0 else 0
    u.save()

@man.command
def listusers():
    'List all user in leaderboard.'
    check_db()
    from database import User
    from os import linesep
    users = User.select()
    print '{} users total{}--'.format(users.count(), linesep)
    for u in users:
        print u.id, u.username, u.points

man.add_command('cleanup', Cleanup)
man.add_command('createdb', CreateDB)

if __name__ == '__main__':
    man.run()
