#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import session, g, Flask, request, abort, json, jsonify, Response

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
            session['cookie']

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
    if userinfo:
        return jsonify({'r': 0, 'user_info': userinfo})
    else:
        return jsonify({'r': 1, 'err': 'unauthorized'})


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


urls = (
    '/song/<int:sid>', 'Song',
)

class Song(RestfulMixins):
    @property
    def client():
        return self._client or WebClient()

    def GET(self, sid):
        m = models.Song({'id': str(sid)})
        m.fetch()
        result = m.toJSON()
        if not result:
            return self.error(404, msg="song_no_found")


class User(RestfulMixins):
    pass


webpy_route(app, urls, locals())


if __name__ == '__main__':
    s = Song()
    print hasattr(s, 'GET')
    print s.GET

