#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for
from turkeyfm import app

@app.route('/', methods=['GET'])
def index():
    """docstring for index"""
    return render_template('index.html')

@app.route('/crossdomain.xml')
def crossdomain():
    return redirect( url_for('static', filename="crossdomain.xml") )

@app.route('/playground')
def pg():
    return render_template('playground/animation.html')


