#!/usr/bin/env python
# -*- coding: utf-8 -*-
import types

from turkeyfm import app
from yafa.redisdb import get_redis
from flask import json

#def sent_job(message, channel=channel_name, redis=redis):
    #if type(message) == types.DictionaryType:
        #message = serializer.dumps(message)
    #return redis.publish(channel, message)


class Manager(object):
    """ Simple redis-based daemon task manager 
    '''
    subscribe message:
    {
        'type': 'subscribe',
        'pattern': None,
        'channel': 'foo',
        'data': b('hello foo')
    },
    just message:
    {
        'type': 'message',
        'pattern': None,
        'channel': 'foo',
        'data': b('hello foo')
    }
    '''
    """

    serializer = json

    def __init__(self):
        """docstring for __init__"""
        self.redis = get_redis(app)
        self.pubsub = self.redis.pubsub()
        self._sub_map = {}
        pass

    def listen(self, channel, callback):
        """
            string:channel
            callback
        """
        self.pubsub.subscribe(channel)
        self._sub_map.update({ channel: callback })

    def unlisten(self, channel):
        self.pubsub.unsubscribe(channel)
        self._sub_map.pop(channel, None)
        pass

    def add_worker(self, worker):
        self.listen(worker.channel, worker.callback)

    def run(self):
        for msg in self.pubsub.listen():
            if msg.get('type') == 'message':
                try:
                    data = self.serializer.loads(msg.get('data'))
                except:
                    data = msg.get('data')
                callback = self._sub_map.get(msg.get('channel'))
                callback(data)
            pass
        pass

    def love(self):
        return self.run()


if __name__ == '__main__':
    make = Manager()
    make.love()

