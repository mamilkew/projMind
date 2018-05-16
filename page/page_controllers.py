from flask import Blueprint, render_template


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def index():
    return render_template("index.html")


@page.route('/hello')
def hello():
    return 'Hello, World'
