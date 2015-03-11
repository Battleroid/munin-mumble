import os
from flask_script import Manager
from rankings import app

app.config.from_object(os.environ['APP_CONFIG'])

manager = Manager(app)

if __name__ == '__main__':
    manager.run()