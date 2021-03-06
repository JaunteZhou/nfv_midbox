#!/usr/bin/python
# -*- coding: utf-8 -*-
#plat.py
import logging
logger = logging.getLogger(__name__)

from flask import Flask, request, jsonify
import json

from midbox import central_unit

app = Flask(__name__)


@app.route("/nfvcmd", methods=['POST'])
def manage():
    logger.debug('Start.')

    if request.method != 'POST':
        return jsonify({"res": "0"}), 400
    if not request.json:
        return jsonify({"res": "0"}), 400

    print(request.json)
    ret = central_unit.proc(request.json)
    # TODO：修改返回值参数，返回给北向管理处

    return jsonify(ret), 201


if __name__ == '__main__':
    app.run()
