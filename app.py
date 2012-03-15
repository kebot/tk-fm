#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import time
from web.contrib.template import render_jinja
import doubanfm
import os
import json
from cache import store

TMP_PATH = '/tmp/morelisten/'
if not os.path.isdir(TMP_PATH):
    os.makedirs(TMP_PATH)

urls = (
    r"/", "More",
    r"/notify", "Notify",
    r"/speaker", "Speaker",
    r"/user/login", "Login",
    r"/audio/(\d+)/(.*)", 'Music',
    )

# _status_stored_in_cookie
render = render_jinja(
        'template',
        encoding='utf-8',
    )


class More(object):
    def __init__(self):
        expire = web.cookies().get('expire')
        if expire and int(expire) > time.time():
            self.cookies = web.cookies()
            self.cookies.update(is_login = True)
            user_name = unicode(self.cookies.get('user_name').decode('utf8'))
            self.cookies.update(user_name = user_name)
        else:
            self.cookies = web.storage()
        self.client = doubanfm.Client(**self.cookies)

    def GET(self):
        songs = self.client._get_song_list()
        return render.index(cookies=self.cookies, songs=songs)


class Speaker(object):
    """ the speaker is the user who play music"""
    def GET(self):
        return render.speaker()


# play - sid
class Notify(object):
    """ the notification: 
            current:
                sid: ---
    """
    def GET(self):
        current = store.getDict('current')
        if not current:
            current = {}
            store.setDict('current', current)
        return json.dumps(current)

    def POST(self):
        sid = web.input().get('sid')
        song = store.getDict(sid)
        current = dict(song=song)
        store.setDict('current', current)


import urllib2
class Music(object):
    def GET(self, sid, url):
        sid = str(sid)
        fp = open(TMP_PATH+sid+'.mp3', 'w+')
        LENGTH = 1024
        url = 'http://' + url
        up = urllib2.urlopen(url)
        for key in up.headers.dict:
            web.header(key, up.headers.dict.get(key))
        for value in up:
            fp.write(value)
            yield value
        fp.close()


class Login(object):
    def POST(self):
        auth = web.input()
        client = doubanfm.Client(auth.get('username'), auth.get('password'))
        if client.is_login:
            cookies = client.to_cookies()
            for cookie in cookies:
                web.setcookie(*cookie)
            return "Login Success..."
        else:
            #@TODO destory cookies
            return "Login Failed..."
            pass

application = web.application(urls, globals())

if __name__ == '__main__':
    application.run()
