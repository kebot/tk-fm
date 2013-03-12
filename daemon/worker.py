#!/usr/bin/env python
# -*- coding: utf-8 -*-

from douban_hack import DoubanFMClient
from turkeyfm.models.song import Song, UserSong
from flask import json
from yafa.redisdb import get_redis

import logging

class BaseWorker(object):
    serializer = json

    def __init__(self, redis=None):
        if not redis:
            self.redis = get_redis()

    def _publish(self):
        if type(message) == types.DictionaryType:
            message = self.serializer.dumps(message)
        return redis.publish(channel, message)


class FavSongWorker(BaseWorker):
    """docstring for FavSongWorker"""
    def __init__(self, login_info=None):
        super(FavSongWorker, self).__init__()
        if login_info is None:
            login_info = self.serializer.loads(self.redis.rpop(self.redis_key))
        self.app = DoubanFMClient(login_info=login_info)

    channel = 'fav_song'
    redis_key = 'job_' + channel

    @classmethod
    def sent(cls, info=None, redis=None):
        if not redis:
            redis = get_redis()
        redis.lpush(cls.redis_key, cls.serializer.dumps(info))
        redis.publish(cls.channel, info)

    @classmethod
    def callback(cls, msg):
        #login_info = cls.serializer.loads(redis.rpop(cls.redis_key))
        worker = cls()
        worker.process()

    def process(self):
        user_info = self.app.json_request('get', 'user_info')
        print 'User_Info', user_info
        liked_num = user_info['liked_num']
        print 'Liked_Sum', liked_num
        response = self.app.json_request('get', 'liked_songs',
                params={'count': liked_num})
        if response['r'] == 0:
            songs = response['songs']
            [self.store_song(song, user_info['user_id']) for song in songs]
        print 'fetch', len(songs), 'for user - ', user_info['user_id']

    def store_song(self, song, uid):
        sid = song.get('sid')
        us = UserSong(uid)
        us.set(sid, UserSong.LIKED)


if __name__ == '__main__':
    threading.Thread(target=main).start()
    sent_job('this is a message', channel_name)
    sent_job({'keith': 'yao'}, channel_name)

