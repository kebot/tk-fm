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
    r"/channel/(\d+)", "Channel",

    r"/song/(\w+)/(\w+)", "Song",
    r"/song/(\w+)", "Song",
    r"/notify", "Notify",

    r"/speaker", "Speaker",
    r"/user/login", "Login",
    r"/user/logout", "Logout",

    r"/audio/(\w+)/(.*)", 'Download',
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

    def GET(self):
        # songs = self.client._get_song_list(channel)
        current = store.getDict('current')
        if not current:
            current = {u"list":[],u"song":{}}
        return render.index(cookies=self.cookies, current=current)

class Channel(object):
    def GET(self, channel=0):
        self.client = doubanfm.Client(**web.cookies())
        return json.dumps(self.client._get_song_list(channel))


class Speaker(object):
    """ the speaker is the user who play music"""
    def GET(self):
        return render.speaker()


class Song(More):
    def GET(self, sid):
        current = store.getDict(sid)
        return json.dumps(current)

    def POST(self, sid, action):
        client = doubanfm.Client(**web.cookies())
        song = doubanfm.Song(client, sid=sid)

        if action == 'bye':
            response = song.bye()
        elif action == 'rate':
            response =  song.rate()
        elif action == 'unrate':
            response =  song.unrate()
        elif action == 'skip':
            response = song.skip()
        else:
            response = {}
            # @TODO throw unsupport action
        return json.dumps(response)


# play - sid
class Notify(object):
    """ the notification:
            current:
                sid: ---

            list: (array)
                [13451, 14890, ...]
    """
    def GET(self):
        current = store.getDict('current')
        if not current:
            current = {}
            store.setDict('current', current)
        return json.dumps(current)


    def POST(self):
        action = web.input().get('action')
        sid = web.input().get('sid')
        current = store.getDict('current')
        current_song_list = current.get('list')
        if current_song_list != None:
            if action == 'remove':
                current_song_list.remove(sid)
            elif action == 'front':
                current_song_list.remove(sid)
                current_song_list.insert(0, sid)
            elif action == 'play':
                current_song_list.remove(sid)
                current.update(song=store.getDict(sid))
            else:
                if not sid in current_song_list:
                    current_song_list.append(sid)
        else:
            current_song_list = []
        current.update(list=current_song_list)
        store.setDict('current', current)
        return self.GET()


import urllib2
class Download(object):
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


def delete_cookies():
    cookies = ['token', 'username', 'user_id', 'expire']
    for cookie in cookies:
        web.setcookie(cookie, '', expires=1)

class Login(object):
    def POST(self):
        auth = web.input()
        client = doubanfm.Client(auth.get('username'), auth.get('password'))
        if client.is_login:
            cookies = client.to_cookies()
            for cookie in cookies:
                web.setcookie(*cookie)
            web.seeother('/')
        else:
            delete_cookies()
            return "Login Failed..."


class Logout(object):
    def GET(self):
        delete_cookies()
        web.seeother('/')

application = web.application(urls, globals())
application.wsgifunc()

if __name__ == '__main__':
    application.run()
