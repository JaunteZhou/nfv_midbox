#!/usr/bin/python3
# -*- coding: utf-8 -*-
#plat.py

from flask import Flask,request
import flask
import json

import central_unit

app = Flask(__name__)

@app.route("/nfvcmd", methods=['POST'])
def manage():
    if request.method == 'POST':
        req_content = json.dumps(request.form)
        print(request.form)

        ret = central_unit.proc(req_content)
        # TODO：修改返回值参数，返回给北向管理处

        ret_json = flask.jsonify(ret[1])
    return ret_json

if __name__=='__main__':
    app.run()