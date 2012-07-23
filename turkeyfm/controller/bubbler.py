#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turkeyfm import app
from flask import request, jsonify

from io import io
# Demo Controller for bubbler project

@app.route('/api/song/<int:sid>/bubblers', method=['GET', 'POST'])
def bubblers_for_song(sid):
    if request.method == 'GET':
        return jsonify([])
    elif request.method == 'POST':
        data =  json.loads(request.data)
        io.publish 's'+str(sid), request.data

