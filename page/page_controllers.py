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


@page.route('/pj-timeline')
def pj_timeline():
    return render_template("pj_timeline.html")

@page.route('/results')
def pj_results():
    return render_template("pj_results.html")