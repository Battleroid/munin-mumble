from flask import Flask, render_template, g
from database import User, db

# flask
app = Flask(__name__)

@app.before_first_request
def setup_db():
    db.connect()
    if not User.table_exists():
        User.create_table()
    db.close()

@app.before_request
def before():
    g.db = db
    g.db.connect()

@app.after_request
def after(resp):
    g.db.close()
    return resp

@app.route('/', methods=('GET',))
def index():
    users = User.select().limit(100).order_by(User.points.desc()).dicts()[:]
    return render_template('index.html', title='Leaderboard', users=users)

if __name__ == '__main__':
    if not User.table_exists():
        User.create_table()
    app.run(debug=True)
