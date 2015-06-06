from flask import Flask, render_template
from database import User

# flask
app = Flask(__name__)

@app.route('/', methods=('GET',))
def index():
    users = User.select().limit(100).order_by(User.points.desc()).dicts()[:]
    return render_template('index.html', title='Leaderboard', users=users)

if __name__ == '__main__':
    if not User.table_exists():
        User.create_table()
