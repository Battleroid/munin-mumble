from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_cache import Cache
from database import User

# flask
app = Flask(__name__)

# cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

# assets
assets = Environment(app)
css = Bundle('css/main.css', 'css/skeleton.css', 'css/normalize.css', output='css/bundled.css')
assets.register('css_min', css)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', error=e)

@app.route('/', methods=('GET',))
def index():
    users = User.select()
    return render_template('index.html', title='Leaderboard', users=users)