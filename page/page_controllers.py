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


@page.route('/donor')
def donor_to_pj():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "donor.json")
    data = json.load(open(json_url))
    # head = data['head']['vars']
    results = data['results']['bindings']
    new_results = {}
    nodes = []
    edges = []

    for result in results:
        # initiate variable
        donor_type = {'name': result.get('class').get('value').split('#')[-1]}
        if result.get('donor') is not None:
            donor_instance = {'name': result.get('donor').get('value').split('#')[-1]}
            country = {'name': result.get('country').get('value').split('#')[-1]}
            donor_name = {'name': result.get('name').get('value')}
        if result.get('project') is not None:
            project = {'name': result.get('project').get('value').split('#')[-1]}

        # --------donor class---------
        if donor_type not in nodes:
            nodes.append(donor_type)
            edge_class = len(nodes) - 1
        else:
            edge_class = nodes.index(donor_type)
        # --------donor category---------
        if result.get('category') is not None:
            donor_subtype = {'name': result.get('category').get('value').split('#')[-1]}
            if donor_subtype not in nodes:
                nodes.append(donor_subtype)
                edge_category = len(nodes) - 1
            else:
                edge_category = nodes.index(donor_subtype)
            # edges.append({'source': edge_class, 'target': edge_category})

            # --------donor instance---------
            if result.get('donor') is not None:
                if donor_instance not in nodes:
                    nodes.append(donor_instance)
                    edge_instance = len(nodes) - 1
                else:
                    edge_instance = nodes.index(donor_instance)
                edges.append({'source': edge_category, 'target': edge_instance})
                nodes.append(country)
                edge_country = len(nodes) - 1
                nodes.append(donor_name)
                edge_name = len(nodes) - 1
                edges.append({'source': edge_instance, 'target': edge_country})
                edges.append({'source': edge_instance, 'target': edge_name})
                if result.get('project') is not None:
                    nodes.append(project)
                    edge_project = len(nodes) - 1
                    edges.append({'source': edge_instance, 'target': edge_project})
        else:
            # --------donor instance no category---------
            if result.get('donor') is not None:
                if donor_instance not in nodes:
                    nodes.append(donor_instance)
                    edge_instance = len(nodes) - 1
                else:
                    edge_instance = nodes.index(donor_instance)
                edges.append({'source': edge_class, 'target': edge_instance})
                nodes.append(country)
                edge_country = len(nodes) - 1
                nodes.append(donor_name)
                edge_name = len(nodes) - 1
                edges.append({'source': edge_instance, 'target': edge_country})
                edges.append({'source': edge_instance, 'target': edge_name})
                if result.get('project') is not None:
                    nodes.append(project)
                    edge_project = len(nodes) - 1
                    edges.append({'source': edge_instance, 'target': edge_project})

    new_results['nodes'] = nodes
    new_results['edges'] = edges
    # print(new_results)
    return render_template("donor_to_pj.html", data=new_results)
