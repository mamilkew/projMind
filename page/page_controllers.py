import os
from flask import Blueprint, render_template, json, request

page = Blueprint('page', __name__, template_folder='templates')
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


@page.route('/')
def index():
    return render_template("index.html")


@page.route('/country-map')
def country_map():
    return render_template("country_map.html")


@page.route('/pj-timeline')
def pj_timeline():
    return render_template("pj_timeline.html")


@page.route('/donor')
def donor_to_pj():
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
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


@page.route('/results')
def pj_results():
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
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


# Done for the staff workflow
# 1. setting up sparql query on /sparql_taxonomy
# 2. submit form (ajax) to /sparql for send query to api
# 3. then call "read_sparql_result()" for transfer pattern(d3js)
# 4. read_sparql_result() is create a file for visualization on /set-taxonomy
@page.route('/set-taxonomy')
def set_taxonomy():
    return render_template("set_taxonomy.html")


@page.route('/sparql_taxonomy')
def sparql_taxonomy():
    # json_url = os.path.join(SITE_ROOT, "static/api", "class_dropdown.json")
    # data = json.load(open(json_url))
    # results = data['results']['bindings']
    relations = {}
    subjects = []
    # for each in results:
    #     for key in (each.keys() | each.keys()):
    #         subjects.append(each[key].get('value').split('#')[-1])
    # subjects = sorted(list(set(subjects)))
    # print(subjects)

    json_url = os.path.join(SITE_ROOT, "static/api", "my_dropdown.json")
    data = json.load(open(json_url))
    results = data['results']['bindings']
    predicates = []
    ranges = []
    for each in results:
        for key in (each.keys() | each.keys()):
            if key == 'class':
                subjects.append(each[key].get('value').split('#')[-1])
            elif key == 'predicate':
                if each.get('range') is not None:
                    xsd = 'http://www.w3.org/2001/XMLSchema'
                    if each['range'].get('value').split('#')[0] == xsd:
                        predicates.append(
                            each['class'].get('value').split('#')[-1] + '#' + each[key].get('value').split('#')[-1])
                    else:
                        predicates.append(
                            each['class'].get('value').split('#')[-1] + '#' + each[key].get('value').split('#')[
                                -1] + '#' +
                            each['range'].get('value').split('#')[-1])
                else:
                    predicates.append(
                        each['class'].get('value').split('#')[-1] + '#' + each[key].get('value').split('#')[-1])
            else:
                ranges.append(each[key].get('value').split('#')[-1])
    subjects = sorted(list(set(subjects)))
    predicates = sorted(list(set(predicates)))
    ranges = sorted(list(set(ranges)))
    print(subjects)
    print(predicates)
    print(ranges)

    relations['subjects'] = subjects
    relations['predicates'] = predicates
    relations['ranges'] = ranges

    return render_template("sparql_taxonomy.html", data=relations)


@page.route('/sparql', methods=['POST'])  # ajax for submit query script
def sparql():
    s = request.form['sellist1']
    p = request.form['sellist2']
    if request.form.get('sellist3') is not None:
        o = request.form['sellist3']
        text = 'SELECT DISTINCT * WHERE { ?name rdf:type aitslt:' + s + ' . ?name aitslt:' + p + ' ?children . optional{?children rdf:type aitslt:' + o + ' .}}'
    else:
        text = 'SELECT DISTINCT * WHERE { ?name rdf:type aitslt:' + s + ' . ?name aitslt:' + p + ' ?children .}'

    prefix = ['PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>',
              'PREFIX owl: <http://www.w3.org/2002/07/owl#>',
              'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>',
              'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>',
              'PREFIX aitslt: <http://www.semanticweb.org/milkk/ontologies/2017/11/testData#>']

    # result will correct if sparql same
    expected = 'SELECT DISTINCT * WHERE { ?name rdf:type aitslt:OrganizationUnit . ?name aitslt:includes ?children . optional{?children rdf:type aitslt:OrganizationUnit .}}'
    # if text == expected:
        # result should be return here!
        # transfer to d3js pattern
        # read_sparql_result()
    return json.dumps({'status': 'OK', 'prefix': prefix, 'query': text})
    # else:
    #     return json.dumps({'status': 'something wrong', 'query': s + p + o})


def read_sparql_result():
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "org_includes_org.json")
    data = json.load(open(json_url))
    results = data['results']['bindings']
    # new_results = {'name': 'SET', 'children': []}
    new_results = {}

    n_results = []
    parents = []
    for each in results:
        for key in (each.keys() | each.keys()):
            if key == 'name':
                parents.append(each[key].get('value').split('#')[-1])
    parents = sorted(list(set(parents)))
    print(parents)

    for parent in parents:
        children = []
        for each in results:
            for key in (each.keys() | each.keys()):
                if key == 'name' and each[key].get('value').split('#')[-1] == parent:
                    children.append(each['children'].get('value').split('#')[-1])
        children = sorted(children)
        # print(children)
        keys = []
        for child in children:
            if child in parents:
                keys.append({'name': child})
            else:
                keys.append({'name': child})
        # print(keys)

        for each in results:
            for key in (each.keys() | each.keys()):
                if key == 'name' and each[key].get('value').split('#')[-1] == parent:
                    add = {'name': parent, 'children': keys}
                    if add not in n_results:
                        n_results.append(add)

        for n in n_results:
            # print('---n---')
            # print(n)
            for c in n.get('children'):
                if c.get('name') in parents:
                    # print('---c---')
                    # print(c)
                    for idx, transitive in enumerate(n_results):
                        if transitive.get('name') == c.get('name'):
                            c['children'] = transitive.get('children')
                            del n_results[idx]  # ลบ กลุ่มที่มายัดไส้ ทิ้ง
                    # print(c)
    # print('============')
    # print(n_results)

    new_results['name'] = 'ROOT'
    new_results['children'] = n_results

    with open("static/data/old/results.json", "w") as fo:
        fo.write(json.dumps(new_results))


# backup
def pee_nut():
    n_results = []
    parents = []
    for each in results:
        for key in (each.keys() | each.keys()):
            if key == 'name':
                parents.append(each[key].get('value').split('#')[-1])
    parents = sorted(list(set(parents)))
    print(parents)

    for parent in parents:
        children = []
        for each in results:
            for key in (each.keys() | each.keys()):
                if key == 'name' and each[key].get('value').split('#')[-1] == parent:
                    children.append(each['children'].get('value').split('#')[-1])
        children = sorted(children)
        print(children)
        keys = []
        for child in children:
            if child in parents:
                keys.append({'name': child})
            else:
                keys.append({'name': child})
        print(keys)

        for each in results:
            for key in (each.keys() | each.keys()):
                if key == 'name' and each[key].get('value').split('#')[-1] == parent:
                    add = {'name': parent, 'children': keys}
                    if add not in n_results:
                        n_results.append(add)
        print(n_results)

    # แค่ทำให้มีแม่ลูก 1 ขั้น ยังซ้อนชั้นไม่ได้
    #
    # children = []
    # for idx, result in enumerate(results):
    #     childrens = []
    #     name1 = result.get('name').get('value').split('#')[-1]
    #     # child1 = {'name': result.get('children').get('value').split('#')[-1]}
    #     for idy, in_result in enumerate(results):
    #         name2 = in_result.get('name').get('value').split('#')[-1]
    #         child2 = {'name': in_result.get('children').get('value').split('#')[-1]}
    #         if name1 == name2:
    #             childrens.append(child2)
    #             # if idx != idy:
    #             #     out.append(idy)
    #     new = {'name': name1, 'children': childrens}
    #     if new not in children:
    #         children.append(new)
    #     print(new)
    # print(children)
