#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request
from turkeyfm import app
from turkeyfm.models import Room as RoomModel

@app.route('/', methods=['GET'])
def index():
    """docstring for index"""
    return render_template('index.html')

# url-pattern '/room/:room.uuid'
# ------------------------ room crud ------------------------------
@app.route('/j/room/<path:rid>', methods=[
    'GET', 'POST', 'UPDATE', 'DELETE', 'PATCH'])
def restful_room(rid):
    response = None
    model = RoomModel(id=rid)
    model.fetch()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'UPDATE':
        pass
    elif request.method == 'DELETE':
        pass


# ------------------------ misc -----------------------------------
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

