from flask import Blueprint, render_template


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def index():
    return render_template("index.html")


@page.route('/country-map')
def country_map():
    return render_template("country_map.html")


@page.route('/set-taxonomy')
def set_taxonomy():
    return render_template("set_taxonomy.html")
