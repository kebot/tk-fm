#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request
from turkeyfm import app

@app.route('/', methods=['GET'])
def index():
    """docstring for index"""
    return render_template('index.html')

@app.route('/crossdomain.xml')
def crossdomain():
    return redirect(url_for('static', filename="crossdomain.xml"))

@app.route('/playground/<path:path>')
def pg(path):
    return render_template('playground/' + path + '.html')

@app.before_request
def before_req():
    if request.endpoint == 'favicon':
        return redirect('http://douban.fm/favicon.ico')

@app.route('/favicon.ico')
def favicon():
    pass

