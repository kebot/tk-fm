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

from .helper import require_api_login, require_web_login
from douban_hack import WebClient, DoubanFMClient as APIClient

from turkeyfm.daemon.worker import FavSongWorker

@app.route('/account/login', methods=['POST'])
def login():
    """
        There is two way of login:
        1. Cookie Based Login with WebClient
        2. API Based Login with DoubanFMClient

        This method
    """
    a = {}
    for key in ['alias', 'form_password', 'captcha_id', 'captcha_solution']:
        if request.json.has_key(key):
            a[key] = request.json[key]
        else:
            return abort(403)
    client = WebClient()

    a.setdefault('remember', 'on')
    response = client.login(**a)
    if response:
        if response.get('r') == 0 and response.get('user_info'):
            session['user_info'] = response.get('user_info')
            session['cookie_info'] = client.to_dict()
    else:
        return abort(404)

    api_client = APIClient()
    api_response = api_client.login(a.get('alias'), a.get('form_password'))
    login_info = api_client.get_login_info()
    if login_info:
        session['api_info'] = login_info
    FavSongWorker.sent(login_info)
    return jsonify(response)


@app.route('/account/new_captcha')
def get_captcha():
    client = WebClient()
    captcha_id, src = client.get_captcha()
    return jsonify({u'captcha_id': captcha_id, u'src': src })


@app.route('/account')
def get_account():
    userinfo = session.get('user_info')
    device_id = session.get('device_id')
    if userinfo:
        return jsonify({'r': 0, 'user_info': dict(userinfo,
            device_id = device_id)})
    else:
        return jsonify({'r': 1, 'err': 'unauthorized'})

# -- finish account -- #
#
# Two way login, /fm/<path:info> will proxy to http://www.douban.fm/j/
# /j/playlist will proxy to http://www.douban.fm/

@app.route('/radio/liked_songs')
@require_api_login
def liked_songs():
    api_user_info = session['api_info']
    print 'api_info in session', api_user_info
    if api_user_info:
        FavSongWorker.sent(api_user_info)
    return '200 OK'


@app.route('/radio/<path:info>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_api_login
def proxy_api(info):
    client = g.api_client
    r = client.request(request.method, info,
            params=dict(request.args or {}), data=dict(request.json or {})
        )
    return Response(response=r.content, status=r.status_code,
            content_type=r.headers.get('content-type', 'application/json'))


@app.route("/fm/mine/playlist", methods=['GET'])
@require_web_login
def proxy_playlist():
    info = 'mine/playlist'
    client = g.web_client
    extra = request.json or {}
    r = client.request(request.method, info, **extra)

    if not r.ok:
        return abort(404)

    response = r.json()

    if response['r'] == 0:
        def parse_song(attrs):
            r_song = models.Song(models.Song.parse(attrs))
            r_song.save()
            return r_song.toJSON()
        response['song'] = [parse_song(attrs) for attrs in response['song']]

    return jsonify(response)

    #return Response(response=r.content, status=r.status_code,
            #content_type=r.headers.get('content-type', 'application/json'))


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

