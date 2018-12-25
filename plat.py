#!/usr/bin/python3
# -*- coding: utf-8 -*-
#plat.py

from flask import Flask, request, jsonify
import json

import central_unit

app = Flask(__name__)

@app.route("/nfvcmd", methods=['POST'])
def manage():
    if request.method != 'POST':
        abort(400)
    if not request.json or not 'title' in request.json:
        abort(400)
    # req_content = json.loads(request.form)
    print(request.json)

    # ret = central_unit.proc(req_content)
    # TODO：修改返回值参数，返回给北向管理处

    # ret_json = flask.jsonify(ret[1])
    return jsonify({"res": "0"}), 201

if __name__=='__main__':
    app.run()