import os
from flask import Blueprint, render_template, json


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
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "export-2.json")
    jsdata = json.load(open(json_url))
    head = jsdata.get('head')
    print(head)
    return render_template("pj_results.html", data=head)
