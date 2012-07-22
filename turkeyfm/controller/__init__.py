#!/usr/bin/env python
# -*- coding: utf-8 -*-
from turkeyfm import app, config, doubanfm
from juggernaut import Juggernaut
from flask import request, session, json, jsonify
from flask.ext.mako import render_template
import time

from utils.redistype import RedisList, RedisHashes

io = Juggernaut()

@app.route('/')
def index():
    current_user_json = jsonify(session).data
    #return render_template('index.html', channels=config.channelInfo)
    return render_template('index.html', current_user=current_user_json,
            channels=json.dumps(config.channelInfo))

def get_client(session):
    expire = session.get('expire')
    if expire and int(expire) > time.time():
        client = doubanfm.Client(user_id=session.get('user_id'),
                expire=session.get('expire'), token=session.get('token'))
    else:
        # Expire
        client = doubanfm.Client()
    return client

@app.route('/api/channel/<channel_id>')
def channel(channel_id):
    client = get_client(session)
    return jsonify(client._get_song_list(channel_id))

@app.route('/api/song/<int:song_id>')
def song(song_id):
    raise NotImplementException
    if request.method == 'GET':
        jsonify()

@app.route('/api/selected', methods=['GET', 'POST', 'PUT', 'DELETE'])
def selected():
    store_key = 'selected'
    store = RedisList(store_key)
    if request.method == 'GET':
        length = len(store)
        if length == 0:
            return jsonify({'song':[], 'r':0, 'total': length})
        else:
            songs = [RedisHashes.getall(sid) for sid in store[:]]
            return jsonify({'song': songs, 'r':0, 'total': length})
    # access data
    if request.data:
        data = json.loads(request.data)
    else:
        data = {}

    if request.method == 'POST':
        if data.get('sid'):
            store.append(data.get('sid'))
            io.publish('selected', {'change': 1})
            return request.data

@app.route('/api/selected/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def selected_modify(sid):
    store_key = 'selected'
    store = RedisList(store_key)

    if request.method == 'PUT':
        raise NotImplementException
        pass
    elif request.method == 'DELETE':
        store.remove(sid)
        io.publish('selected', {'change': 1})
        return jsonify(request.data)
    return jsonify({'r':1, 'err': 'not support'})




@app.route('/api/login', methods=['POST'])
def login():
    username, password = [request.form.get(key) for key in ['username', 'password']]
    if username and password:
        # if user alread login xxx return hash
        if username == session.get('email'):
            return jsonify(session)
        client = doubanfm.Client(username, password)
    else:
        return jsonify({'r': 1, 'err': 'username and password required'})
    if client.is_login:
        session.update(client.to_store())
        return jsonify(client.to_store())
    else:
        logout()
        return jsonify(client.get_error())
        #return jsonify({'r': 1, 'err': 'wrong password or username.'})
    # redirect(url_for('index'))

@app.route('/api/logout')
def logout():
    keys=['expire', 'user_id', 'token', 'user_name']
    for key in keys:
        session.pop(key, None)
    return jsonify({'r': 1})
    #redirect(url_for('index'))


