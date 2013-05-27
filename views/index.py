#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for, request, jsonify
from turkeyfm import app
from turkeyfm.models import Room as RoomModel
from turkeyfm.models.song import Song as SongModel
from yafa.redisdb import get_redis

@app.route('/ui', methods=['GET'])
def ui():
    return render_template('ui.html')

@app.route('/<path:url>', methods=['GET'])
@app.route('/', methods=['GET'])
def index(url=None):
    """All routes will be proxy in front-end."""
    return render_template('index.html')

#@app.route('/ui', methods=['GET'])
#def index():
    #return render_template('ui.html')

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

# -----------------------------------------------------------------
redis_client = get_redis()
@app.route('/j/topsongs', methods=['GET'])
def topsongs():
    count = 20
    r = []
    for i in redis_client.keys('song-*'):
        m = SongModel(id=i[5:])
        r.append(m.toJSON())
    return jsonify(songs=r)

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

