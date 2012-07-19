# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, Flask, request, session, json, jsonify

# from flask.views import View
import time
import config
import juggernaut
import doubanfm

# Create a flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
            channels=config.channelInfo, current=dict(song=''))

io = juggernaut.Juggernaut()

# Ajax interfaces.

def get_client(session):
    expire = session.get('expire')
    if expire and int(expire) > time.time():
        client = doubanfm.Client(session.from_keys(
            ['user_id', 'expire', 'token']))
    else:
        # Expire
        client = doubanfm.Client()
    return client

@app.route('/api/channel/<int:channel_id>')
def channel(channel_id):
    client = get_client(session):
    return json.dumps(client._get_song_list(channel_id))

@app.route('/api/song/<int:song_id>')
def song(song_id):
    if request.method == 'GET':
        jsonify()

@app.route('/api/login')
def login():
    username, password = [form.get(key) for key in ['username', 'password']]
    if username and password:
        client = doubanfm.Client(username, password)
    if client.is_login:
        session.update(client.to_store)
    else:
        return logout()
    redirect(url_for('index'))

@app.route('/api/logout')
def logout():
    keys=['expire', 'user_id', 'token', 'user_name']
    for key in keys:
        session.pop(key, None)
    redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
