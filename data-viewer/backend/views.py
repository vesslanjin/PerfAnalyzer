# Intel Sample Source Code License
#
# Copyright(c) 2015-2020 Intel Corporation. All rights reserved.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, sys, json

from flask import Flask, render_template, redirect, url_for, Response, request, make_response
from flask import jsonify
from flask_cors import CORS

from popo import MyEncoder

import config_service
import cpi_service


app = Flask(__name__)
app.config["SECRET_KEY"] = "111111"                   #A secret key is required to use CSRF.
cors = CORS(app, resources={"/*": {"origins": "*"}})  # 跨域授权


# Hello World
@app.route('/helloworld')
def helloworld():
    return 'Hello, world.'

# Rendering Frontend
@app.route('/')
def index():
    return render_template('index.html')


# Restful APIs
@app.route('/settings')
def settings():
    settings = config_service.get_settings()
    return json.dumps(settings)

@app.route('/cpi/model', methods=['POST'])
def cpi_model():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        response = cpi_service.build_cpi_model(config_ids)
    resp = make_response(jsonify(response))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/cpi/list', methods=['POST'])
def cpi_list():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        cpi_service.build_tb_cpi(config_ids)                             #exec 'build_tb_cpi'
        response = cpi_service.cpi_details_list(config_ids)
    resp = make_response(json.dumps(response, cls=MyEncoder))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/cpi/scaling/corefreq', methods=['POST'])
def cpi_scaling_corefreq():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        legends_dic = config_service.config_ids_spliting(config_ids, member='core_frequency')
        response = cpi_service.core_frequency_scaling(legends_dic)
    resp = make_response(jsonify(response))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/cpi/scaling/corenum', methods=['POST'])
def cpi_scaling_corenum():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        legends_dic = config_service.config_ids_spliting(config_ids, member='cores')
        response = cpi_service.core_num_scaling(legends_dic)
    resp = make_response(jsonify(response))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/cpi/scaling/uncorefreq', methods=['POST'])
def cpi_scaling_uncorefreq():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        legends_dic = config_service.config_ids_spliting(config_ids, member='uncore_frequency')
        response = cpi_service.uncore_frequency_scaling(legends_dic)
    resp = make_response(jsonify(response))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/cpi/scaling/llc', methods=['POST'])
def cpi_scaling_llc():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        legends_dic = config_service.config_ids_spliting(config_ids, member='llc')
        response = cpi_service.llc_mb_scaling(legends_dic)
    resp = make_response(jsonify(response))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/performance/modeling/glm', methods=['POST'])
def performance_modeling_glm():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        config_ids = config_service.get_config_ids(o)
        response = cpi_service.performance_modeling_glm(config_ids)
    resp = make_response(json.dumps(response, cls=MyEncoder))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

@app.route('/performance/evaluation/glm', methods=['POST'])
def performance_evaluation_glm():
    response = {}
    if request.method != 'POST':
        pass
    else:
        o = json.loads(request.get_data())
        response = cpi_service.performance_evaluation_glm(o)
    resp = make_response(json.dumps(response, cls=MyEncoder))
    resp.headers['Content-type'] = 'application/json;charset=utf-8'
    return resp

# main
if __name__ == '__main__':
    app.run()
