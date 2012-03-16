#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import time
from web.contrib.template import render_jinja
import doubanfm
import os
import json
from cache import store
import config

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TMP_PATH = '/tmp/morelisten/temp/'
AUDIO_PATH = BASE_PATH + '/static/audio/'

if not os.path.isdir(TMP_PATH): 
    os.makedirs(TMP_PATH)

if not os.path.isdir(AUDIO_PATH):
    os.makedirs(AUDIO_PATH)

urls = (
    r"/", "More",
    r"/(\d+)", "More",

    r"/notify", "Notify",
    r"/notify", "Notify",

    r"/speaker", "Speaker",
    r"/user/login", "Login",
    r"/user/logout", "Logout",

    r"/audio/(\d+)/(.*)", 'Music',
    )

# _status_stored_in_cookie
render = render_jinja(
        'template',
        encoding='utf-8',
    )

render._lookup.globals.update(
                channels=config.channelInfo)


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

    def GET(self, channel=0):
        songs = self.client._get_song_list(channel)
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

            queue: (array)
                [13451, 14890, ...]
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
        TMP_FILE_NAME = TMP_PATH+sid+'.mp3.tmp'
        FILE_NAME = AUDIO_PATH+sid+'.mp3'
        if os.path.exists(FILE_NAME):
            web.seeother('/static/audio/%s.mp3' % sid)
        else:
            fp = open(TMP_FILE_NAME, 'w+')
            LENGTH = 1024
            url = 'http://' + url
            up = urllib2.urlopen(url)
            for key in up.headers.dict:
                web.header(key, up.headers.dict.get(key))
            for value in up:
                fp.write(value)
                yield value
            fp.close()
            os.rename(TMP_FILE_NAME, FILE_NAME)


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
