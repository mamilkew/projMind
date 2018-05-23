import os
from flask import Blueprint, render_template, json, url_for


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def index():
    return render_template("index.html")


@page.route('/country-map')
def country_map():
    return render_template("country_map.html")


@page.route('/set-taxonomy')
def set_taxonomy():
    # url_for('static', filename='data/old/civil.json')
    return render_template("set_taxonomy.html")


@page.route('/pj-timeline')
def pj_timeline():
    return render_template("pj_timeline.html")


@page.route('/results')
def pj_results():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "export-2.json")
    data = json.load(open(json_url))
    results = data['results']['bindings']
    new_results = {}
    nodes = []
    edges = []
    for result in results:
        nodes.append({'name': result['project']['value'].split('#')[-1]})
        project = len(nodes) - 1
        nodes.append({'name': result['donor']['value'].split('#')[-1]})
        donor = len(nodes) - 1
        nodes.append({'name': result['type']['value'].split('#')[-1]})
        type = len(nodes) - 1
        nodes.append({'name': result['country']['value'].split('#')[-1]})
        country = len(nodes) - 1
        nodes.append({'name': result['cmmt']['value']})
        cmmt = len(nodes) - 1
        edges.append({'source': project, 'target': donor})
        edges.append({'source': donor, 'target': type})
        edges.append({'source': donor, 'target': country})
        edges.append({'source': donor, 'target': cmmt})


    # head = jsdata.get('head')
    new_results['nodes'] = nodes
    new_results['edges'] = edges
    # print(new_results)
    # js_results = json.dumps(new_results)
    # print(js_results)
    return render_template("pj_results.html", data=new_results)
