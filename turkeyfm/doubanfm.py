#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is an unoffical client for DoubanFM.
import urllib2
import urllib
import web
import json
import time
from cache import store

def wrap_song_list(func):
    def wrapper(*argc, **argv):
        songs = func(*argc, **argv)
        return [Song(argc[0], song) for song in songs]
    return wrapper


class Client(object):
    _base_dict = dict(app_name='radio_desktop_win', version='100')
    _current_playing_song = None
    _current_channel = None

    def __init__(self, username=None, password=None, **extra):
        self._status = None
        if username and password:
            self._username = username
            self._password = password
            self._login()
        else:
            _flag_has_key = True
            must_have_keys=['expire', 'user_id', 'token']
            for key in must_have_keys:
                if not extra.has_key('key'):
                    _flag_has_key = False
            if _flag_has_key:
                self._status = extra

    @property
    def is_login(self):
        return self._status is not None

    def to_cookies(self):
        cookies = []
        keys=['expire', 'user_id', 'token', 'user_name']
        expire = int(self._status.get('expire')) - time.time()
        for key in keys:
            cookies.append((key, self._status.get(key), expire))
        return cookies


    def _login(self):
        self._status = self._do_login()
        if self._status.get('r') == 0:
            self._base_dict.update(user_id=self._status.get('user_id'),\
                    expire=self._status.get('expire'), token=\
                    self._status.get('token'))

    def _do_login(self):
        """ do login, and return a object """
        login_url = "http://www.douban.com/j/app/login"
        login_info = urllib.urlencode(dict(self._base_dict,
            email=self._username, password=self._password))
        handle = urllib2.urlopen(login_url, login_info)
        response = handle.read()
        handle.close()
        return json.loads(response)

    def request(self, **extra):
        # @TODO channel is required.
        if not extra.get('channel'):
            extra.update(channel=0)
        the_url = 'http://www.douban.com/j/app/radio/people'
        get_param = urllib.urlencode(dict(self._base_dict, **extra))
        get_url = the_url + '?' + get_param
        response = json.loads(urllib2.urlopen(get_url).read())
        if response.get('song'):
            for song in response.get('song'):
                store.setDict(song.get('sid'), song)
        return response


    def _get_song_list(self, channel=1):
        #channel = channel or self._current_channel or default_channel
        return self.request(type='n', channel=channel)#.get('song')

class Song():
    def __init__(self, client=None, data=None, **opt):
        """ create a new song """
        if data:
            url = u'/audio/%s/%s' % (data.get('sid', ''),\
                    data.get('url', '')[7:])
            data.update(url=url)

            self._data = data
            self.store(data)

        if client:
            self._client = client

        if opt.has_key('sid'):
            sid = opt.get('sid')
            self.restore(sid)

    def store(self, data):
        store.setDict(data.get('sid'), data)

    def restore(self, sid):
        self._data = store.getDict(sid)

    def setClient(self, c):
        self._client = c

    def bye(self):
        """ do not play this song again """
        return self._client.request(type='b', sid=self.sid)

    def rate(self):
        """ I like this song """
        return self._client.request(type='r', sid=self.sid)

    def unrate(self):
        """ unlike this song """
        return self._client.request(type='u', sid=self.sid)

    def skip(self):
        """ skip this song """
        return self._client.request(type='s', sid=self.sid)

    #@property
    #def parse_url(self):
    #    return u'/audio/%s/%s' % (self._data.get('sid', ''),\
    #            self._data.get('url', '')[7:])

    def __getattr__(self, name):
        if self._data:
            return self._data.get(name)
        else:
            return None

    def __repr__(self):
        return u"<Song %s>" % self.title


if __name__ == '__main__':
    username = ''
    password = ''
    c = Client(username, password)
    songs = c._get_song_list()
    for song in songs:
        print song.url()
