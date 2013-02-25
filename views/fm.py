#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path

from flask import (session, g, Flask, request, abort, json, jsonify,
        Response, redirect, url_for)
import requests

from yafa.routing import webpy_route
from yafa.restful import RestfulMixins

from turkeyfm import app
from turkeyfm import models

from douban_hack import WebClient

@app.route('/account/login', methods=['POST'])
def login():
    client = WebClient()
    a = {}
    for key in ['alias', 'form_password', 'captcha_id', 'captcha_solution']:
        if request.json.has_key(key):
            a[key] = request.json[key]
        else:
            return abort(403)
    a.setdefault('remember', 'on')
    response = client.login(**a)
    if response:
        if response.get('r') == 0 and response.get('user_info'):
            session['user_info'] = response.get('user_info')
            session['cookie_info'] = client.to_dict()

        return jsonify(response)
    else:
        abort(404)


@app.route('/account/new_captcha')
def get_captcha():
    # a = requests.get('http://douban.fm/j/new_captcha')
    client = WebClient()
    captcha_id, src = client.get_captcha()
    return jsonify({u'captcha_id': captcha_id, u'src': src })


@app.route('/account')
def get_account():
    userinfo = session.get('user_info')
    device_id = session.get('device_id')
    if userinfo:
        return jsonify({'r': 0, 'user_info': userinfo, 'device_id':
            device_id})
    else:
        return jsonify({'r': 1, 'err': 'unauthorized'})

# -- finish account -- #

@app.route('/fm/mine/playlist', methods=['GET'])
def proxy_playlist():
    info = 'mine/playlist'
    client = WebClient(cookies=session.get('cookie_info', {}))
    extra = request.json or {}
    r = client.request(request.method, info, **extra)
    if r.ok:
        json = r.json()
        if json['r'] == 0:
            for song in json['song']:
                r_song = models.Song(song)
                r_song.save()
        return Response(response=r.content, status=r.status_code,
                content_type=r.headers.get('content-type', 'application/json'))
    else:
        return abort(404)


@app.route('/fm/<path:info>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_tofm(info):
    client = WebClient(cookies=session.get('cookie_info', {}))
    extra = request.json or {}
    r = client.request(request.method, info, **extra)
    if r.ok:
        return Response(response=r.content, status=r.status_code,
                content_type=r.headers.get('content-type', 'application/json'))
    else:
        return abort(404)


TMP_PATH = '/tmp/turkeyfm/'
AUDIO_PATH = path.join(app.static_folder, 'audio')

try:
    os.makedirs(TMP_PATH)
    os.makedirs(AUDIO_PATH)
except OSError:
    pass

@app.route('/audio/<int:sid>/<path:url>')
def audio(sid, url):
    sid = str(sid)
    tmp_name = TMP_PATH + sid + '.mp3.tmp'
    filename = path.join(AUDIO_PATH, sid + '.mp3')

    if path.exists(filename):
        return redirect(url_for('static', filename="audio/" + sid + '.mp3'))
    else:
        url = 'http://' + url
        def generate():
            buffer_size = 10
            r = requests.get(url, stream=True)
            fp = open(tmp_name, 'w+')
            app.logger.info("Open %s for writing", tmp_name)
            while True:
                buf = r.raw.read(buffer_size)
                if not buf:
                    break
                fp.write(buf)
                yield buf
            fp.close()
            app.logger.info("Rename from %s to %s" , tmp_name, filename)
            os.rename(tmp_name, filename)
        return Response(generate(), mimetype='audio/mpeg')


urls = (
    '/song/<int:sid>', 'Song',
)

class Song(RestfulMixins):
    @property
    def client():
        return self._client or WebClient()

    def GET(self, sid):
        print sid
        m = models.Song(id=str(sid))
        m.fetch()
        result = m.toJSON()
        if not result:
            return self.error(404, msg="song_no_found")
        return jsonify(result)


class User(RestfulMixins):
    pass


webpy_route(app, urls, locals())


if __name__ == '__main__':
    s = Song()
    print hasattr(s, 'GET')
    print s.GET

