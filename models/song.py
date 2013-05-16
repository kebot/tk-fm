#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel, get_redis_client


class Song(RedisModel):
    __prefix__ = 'song'
    id_attribute = 'sid'

    @staticmethod
    def parse(attributes, **options):
        """ parse attributes from server """
        length = attributes.get('length')
        if length:
            attributes.__setitem__('length', length * 1000)
        return attributes

    def toJSON(self,  **kwargs):
        """@todo: Docstring for toJSON

        :**kwargs: @todo
        :returns: @todo
        """
        attributes = super(Song, self).toJSON(**kwargs)

        if not attributes.get(self.id_attribute):
            return {}

        is_like = 0
        if kwargs.get('uid') is not None:
            is_like = is_like_the_song(kwargs.get('uid'), self.id)

        attributes.update({'like': is_like})
        return attributes


class Channel(RedisModel):
    __prefix__ = 'channel'


SONG_LIKED = 1
SONG_BANDED = -1
SONG_UNKNOW = 0

def is_like_the_song(uid, sid, status=None,redis_client=None):
    """get relationship for song and user"""
    prefix = 'user-song'
    redis_key = "%s-%s" % (prefix, str(uid))
    if not redis_client:
        redis_client = get_redis_client()

    if status is None:
        if redis_client.hexists(redis_key, sid):
            return int(redis_client.hget(redis_key, sid))
        else:
            return SONG_UNKNOW
    else:
        if status in [SONG_BANED, SONG_LIKED, SONG_UNKNOW]:
            return int(redis_client.hset(redis_key, sid, status))

# user -> like -> song

# the new relationship api will be instead whis class
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

