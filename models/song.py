#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel

class Song(RedisModel):
    __prefix__ = 'song'
    id_attribute = 'sid'

class Channel(RedisModel):
    __prefix__ = 'channel'

#class SongList(RedisCollection)

if __name__ == '__main__':
    info = {
      "album": "In Today Already Walks Tomorrow",
      "r": 0,
      "artist": "Sleepmakeswaves",
      "song_name": "So That The Children Will Always Shout Her Name",
      "cover": "http://img3.douban.com/lpic/s2981473.jpg",
      "id": "1381723"
    }
    model = Song(info)
    model.redis_client.flushall()
    assert model.redis_key == "song-1381723"
    model.save()

    model2 = Song({'id': '1381723'})
    model2.fetch()
    assert model2.toJSON() == model.toJSON()

