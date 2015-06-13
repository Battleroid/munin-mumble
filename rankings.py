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
    all_users = User.select().order_by(User.points.desc())
    all_users_dict = all_users.dicts()[:]
    worst_user = all_users_dict[-1]
    total_users = all_users.count()
    total_points = sum(p['points'] for p in all_users_dict)
    time_spent = dict(days='{:,d}'.format(((total_points * 5) // 60) // 24), hours='{:,d}'.format(((total_points * 5) // 60) % 24))
    return render_template('index.html', title='Leaderboard', users=all_users_dict[:100], total_users=total_users, total_points='{:,d}'.format(total_points), time_spent=time_spent, worst_user=worst_user)

if __name__ == '__main__':
    if not User.table_exists():
        User.create_table()
    app.run(debug=True)
