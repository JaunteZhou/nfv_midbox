#!/usr/bin/python3
# -*- coding: utf-8 -*-
#plat.py

from flask import Flask,request
import show_all
import json

import central_unit

app=Flask(__name__)

@app.route("/nfvcmd")
def manage():
    req_content = json.dumps(request.form)
    print(request.form)

    central_unit.proc(req_content)


if __name__=='__main__':
    app.run()