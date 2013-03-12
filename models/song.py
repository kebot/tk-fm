#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel, get_redis_client


class Song(RedisModel):
    __prefix__ = 'song'
    id_attribute = 'sid'


class Channel(RedisModel):
    __prefix__ = 'channel'


class UserSong():
    __prefix__ = 'usersong'
    LIKED = 1
    BANED = -1
    UNKNOW = 0

    # 'usersong-<uid>'
    def __init__(self, uid, redis_client=None):
        self.redis_key = self.__prefix__ + '-' + str(uid)
        if not redis_client:
            redis_client = get_redis_client()
        self.redis_client = redis_client


    def get(self, sid):
        if self.redis_client.hexists(self.redis_key, sid):
            return self.redis_client.hget(self.redis_key, sid)
        else:
            return self.UNKNOW

    def set(self, sid, status):
        assert status in [self.BANED, self.LIKED, self.UNKNOW]
        return self.redis_client.hset(self.redis_key, sid, status)


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

