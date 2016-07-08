from flask import Blueprint, jsonify, Response, render_template, url_for, request
from itertools import groupby
from operator import itemgetter
from os.path import join, dirname
import json, os

import requests
import uritemplate
import psycopg2

from . import util

blueprint = Blueprint('Metro-Extracts', __name__)

def load_cities(filename):
    '''
    '''
    with open(filename) as file:
        cities = json.load(file)
    
    return cities

cities = load_cities(join(dirname(__file__), '..', 'cities.json'))

def apply_blueprint(app, url_prefix):
    '''
    '''
    app.register_blueprint(blueprint, url_prefix=url_prefix)

@blueprint.route('/')
@util.errors_logged
def index():
    ordered_cities = sorted(cities, key=itemgetter('country'))
    metros_tree = list()
    
    for (country, sub_cities) in groupby(ordered_cities, itemgetter('country')):
        sub_metros = list()
        
        for sub_city in sorted(sub_cities, key=itemgetter('name')):
            sub_city['href'] = url_for('Metro-Extracts.get_metro', metro_id=sub_city['id'])
            sub_metros.append(sub_city)
        
        metros_tree.append({'country': country, 'metros': sub_metros})
    
    return render_template('index.html', metros_tree=metros_tree, util=util)

@blueprint.route('/cities.geojson')
@util.errors_logged
def get_cities_geojson():
    features = list()
    
    for city in cities:
        x1, y1, x2, y2 = [float(city['bbox'][k])
                          for k in ('left', 'bottom', 'right', 'top')]

        feature = dict(type='Feature', id=city['id'])
        #feature['bbox'] = [x1, y1, x2, y2]
        feature['geometry'] = dict(type='Polygon')
        feature['geometry']['coordinates'] = [[[x1, y1], [x1, y2], [x2, y2], [x2, y1], [x1, y1]]]
        feature['properties'] = dict(name=city['id'], display_name=city['name'])
        feature['properties']['href'] = url_for('Metro-Extracts.get_metro', metro_id=city['id'])
        features.append(feature)

    return jsonify(dict(features=features))

@blueprint.route('/cities-extractor.json')
@util.errors_logged
def get_cities_extractor_json():
    ordered_cities = sorted(cities, key=itemgetter('region'))
    regions_dict = dict()
    
    for (region, sub_cities) in groupby(ordered_cities, itemgetter('region')):
        ids, bboxes = zip(*[(sc['id'], sc['bbox'])
                            for sc in sorted(sub_cities, key=itemgetter('id'))])

        cities_dict = dict([(id, dict(bbox=bbox)) for (id, bbox) in zip(ids, bboxes)])
        
        tops, lefts, bottoms, rights \
            = zip(*[map(float, (b['top'], b['left'], b['bottom'], b['right']))
                    for b in bboxes])
        
        region_bbox = dict(top=str(max(tops + bottoms)),
                           left=str(min(lefts + rights)),
                           bottom=str(min(tops + bottoms)),
                           right=str(max(lefts + rights)))
        
        regions_dict[region] = dict(bbox=region_bbox, cities=cities_dict)

    return jsonify(regions=regions_dict)

@blueprint.route('/metro/<metro_id>/')
@blueprint.route('/metro/<metro_id>/<wof_id>/<wof_name>/')
@util.errors_logged
def get_metro(metro_id, wof_id=None, wof_name=None):
    with open('cities.json') as file:
        cities = json.load(file)
        metro = {c['id']: c for c in cities}[metro_id]
    
    return render_template('metro.html', metro=metro, wof_id=wof_id,
                           wof_name=wof_name, util=util)

@blueprint.route('/wof/<id>.geojson')
@util.errors_logged
def wof_geojson(id):
    ''' Proxy requests to http://whosonfirst.mapzen.com/spelunker/id/{id}.geojson
    '''
    template = 'http://whosonfirst.mapzen.com/spelunker/id/{id}.geojson'
    url = uritemplate.expand(template, dict(id=id))
    wof_resp = requests.get(url)

    headers = {key: val for (key, val) in wof_resp.headers.items()
               if key in ('Content-Type', 'Content-Length')}
    
    return Response(wof_resp.content, headers=headers)
