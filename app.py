from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
