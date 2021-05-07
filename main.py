#!/usr/bin/env python3

import re
from flask import Flask, request, send_from_directory, render_template, Response
from pathlib import Path
import sys
sys.path.append('configs')
from vars import *

import requests
import xmltodict

app = Flask(__name__, template_folder="templates")
current_dir = Path(__file__)

SERIAL_NUM_RE = re.compile(r"PID:(?P<product_id>\w+(?:-\w+)*),VID:(?P<hw_version>\w+),SN:(?P<serial_number>\w+)")

def work_request(host, type="device_info"):
    url = f"http://{host}/pnp/WORK-REQUEST"
    with open(current_dir / f"{type}.xml") as f:
        data = f.read()
    return requests.post(url, data)


def get_device_info(host):
    url = f"http://{host}/pnp/WORK-REQUEST"

@app.route('/test-xml')
def test_xml():
    result = render_template('load_config.xml', correlator_id="123", config_filename="test.cfg", udi="123", http_server="192.168.195.115:8080")
    return Response(result, mimetype='text/xml')


@app.route('/')
def root():
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print('SOURCE-ADDRESS:%s' % src_add)
    return 'Hello Stream!'

@app.route('/configs/<path:path>')
def serve_configs(path):
    return send_from_directory('configs', path)


@app.route('/images/<path:path>')
def serve_sw_images(path):
    return send_from_directory('sw_images', path)


@app.route('/pnp/HELLO')
def pnp_hello():
    return '', 200


@app.route('/pnp/WORK-REQUEST', methods=['POST'])
def pnp_work_request():
    src_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    data = xmltodict.parse(request.data)
    correlator_id = data['pnp']['info']['@correlator']
    udi = data['pnp']['@udi']
    udi_match = SERIAL_NUM_RE.match(udi)
    serial_number = udi_match.group('serial_number')
    try: 
      config_file = DEVICES[serial_number][config-filename]
      jinja_context = {
          "udi": udi,
          "correlator_id": correlator_id,
          "config_filename": config_file,
          "http_server" : HTTP_SERVER,
      }
      result_data = render_template('load_config.xml', **jinja_context)
      print("Loading " + config_filename + " on " + request.environ['REMOTE_ADDR'] )
      return Response(result_data, mimetype='text/xml')
    except: 
      sys.stderr.write("Unable to load " + config_filename + " on " + request.environ['REMOTE_ADDR'] + " ("+serial_number+")\n")
      return ''
    else: 
      print("autre")
      return ''


@app.route('/pnp/WORK-RESPONSE', methods=['POST'])
def pnp_work_response():
    print(request.data)
    data = xmltodict.parse(request.data)
    correlator_id = data['pnp']['response']['@correlator']
    udi = data['pnp']['@udi']
    jinja_context = {
        "udi": udi,
        "correlator_id": correlator_id,
    }
    result_data = render_template('bye.xml', **jinja_context)
    return Response(result_data, mimetype='text/xml')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
