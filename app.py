from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main.main_controllers import main

app = Flask(__name__,
            instance_relative_config=True,
            template_folder='templates')

POSTGRES = {
    'user': 'milkk',
    'pw': '',
    'db': 'bookshelf',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


# enable jinja2 extensions - i.e. continue in for loops
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.register_blueprint(main, url_prefix='/')


@app.route('/hello')
def hello():
    return 'Hello, World'


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
