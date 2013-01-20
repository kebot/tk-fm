#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import session, g, Flask, request, abort, json

from yafa.routing import webpy_route
from yafa.restful import RestfulMixins

from turkeyfm import app
from turkeyfm import models


urls = (
    '/song/<int:sid>', 'Song',
)


class Song(RestfulMixins):

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

