#!/usr/bin/env python
# -*- coding: utf-8 -*-

# /songs/

from turkeyfm.models import Song

if __name__ == '__main__':
    info = {
      "album": "In Today Already Walks Tomorrow",
      "r": 0,
      "artist": "Sleepmakeswaves",
      "song_name": "So That The Children Will Always Shout Her Name",
      "cover": "http://img3.douban.com/lpic/s2981473.jpg",
      "sid": "1381723"
    }
    model = Song(info)
    model.redis_client.flushall()

    assert model.redis_key == "song-1381723"
    model.save()





