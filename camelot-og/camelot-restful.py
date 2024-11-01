'''
Created on 06-Dec-2018

@author: smaturi
'''

from flask import Flask, request, make_response, abort
from flask_restful import Resource, Api, reqparse
import json

import camelot
from camelot import CamelotError, camlogger
from flask.json import jsonify
import base64
import logging
import argparse

app = Flask('CamelotHttpServer')
api = Api(app)

log = camlogger.getLogger(__name__)
camlogger.setLevel(logging.INFO)

def get_cam_server(ip, port):
    try:
        srv = camelot.get_camelot_server(ip, int(port))
    except CamelotError as exp:
        srv = camelot.create_camelot_server(ip, int(port))
    return srv

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/server/getversion', methods=['POST'])
def get_server_version():
    if not request.json:
        abort(400)
    
    ip = request.json.get('ip')
    port = int(request.json.get('port'))
    version = request.json.get('vesrion')
    
    srv = get_cam_server(ip, port)
    
    return srv.get_server_version()


@app.route('/server/getcompatversions', methods=['POST'])
def get_compat_version():
    if not request.json:
        abort(400)
    
    ip = request.json.get('ip')
    port = int(request.json.get('port'))
    #version = request.json.get('vesrion')
    print("ip = {0}, port= {1}".format(ip,port))

    srv = get_cam_server(ip, port)
    
    return jsonify(srv.get_compat_versions())

@app.route('/server/createep', methods=['POST'])
def create_ep():
    if not request.json:
        abort(400)
    
    ip = request.json.get('ip')
    port = int(request.json.get('port'))
    version = request.json.get('vesrion')
    ep_type = request.json.get('ep_type', 'sipx')
    ep_args = request.json.get('ep_args', [])
    ep_named_args = request.json.get('ep_named_args', {})
    
    srv = get_cam_server(ip, port)
    
    ep = srv.create_new_endpoint(ep_type, *ep_args, **ep_named_args)
    
    ep_ref = base64.encodestring(ep.get_ref().replace('::camelot-og::', ''))
    
    return jsonify(ep_ref.strip())

@app.route('/endpoint/<ep_ref>/<action>', methods=['POST'])
def endpoint_action(ep_ref, action):
    decodef_ep_ref = base64.decodestring(ep_ref)
    decodef_ep_ref_list = decodef_ep_ref.split(':')
    ip = decodef_ep_ref_list[0]
    port = int(decodef_ep_ref_list[1])
    ep_id = decodef_ep_ref_list[2]
    
    srv = get_cam_server(ip, port)
    
    ep = srv.get_endpoint(ep_id)
        
    func = eval("ep.{}".format(action))
    
    log.info('Invoking method: {}'.format(func))
    
    # executing required action
    try:
        if hasattr(request, "json") and request.json:
            resp = func(**request.json)
        else:
            resp = func()
    except CamelotError as exp:
        log.exception(exp)
        return make_response(jsonify({'error': '%r' % exp}), 417)
    
    log.info('Response received for: {}, is: {}'.format(func, resp))
    
    return jsonify(resp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments required for Camelot-Restful')
    parser.add_argument('--ip', default='0.0.0.0',
                        help='Specific IP to be used for hosting REST server - (default: 0.0.0.0)')
    parser.add_argument('--port', default='7755',
                        help='Port on which server would run/available - (default: 7755)')
    args = parser.parse_args()
    log.info('Server About to Start on: {}'.format(args))
    app.run(host=args.ip, port=args.port)