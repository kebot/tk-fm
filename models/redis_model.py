#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A storage in redis.

ps: in 2012, I begins writing this code. Now it's 2013! Happy New Year!
"""

from types import DictType, StringTypes
from flask import g, json as serializer
from redis import Redis

# in flask, you can either access the redis_client from `g.redis_client`
redis_client = None

class RedisModel(object):
    """Simple redis hash based model, inspired by Backbone.Model.
        redis hashes are simple key-string_value storage.
        so you need to serialize the values in order to store more types,
        the serializer need to be json-like(json, yaml, msgpack and more).

>>> RedisModel(prefix='song', id='369918')
"<RedisModel(song-369918)>"
>>> RedisModel({'id': 369918}, prefix='song')
"<RedisModel(song-369918)>"

    """
    id_attribute = 'id'

    def __init__(self, attributes=None, redis_client=None, **options):
        self.attributes = {}
        self.id = None

        if attributes:
            if attributes.__len__() == 1 and self.id_attribute in attributes:
                self.id = attributes.get(self.id_attribute)
            else:
                self.set(attributes)
        elif 'id' in options:
            self.id = options.get('id')

        if not hasattr(self, '__prefix__'):
            if 'prefix' in options:
                self.__prefix__ = options.get('prefix')
            else:
                self.__prefix__ = self.__class__.__name__

        if not redis_client:
            try:
                self.redis_client = g.redis_client
            except (RuntimeError, AttributeError):
                # you are working outside the request context
                # Create a new RedisClient using the default config
                self.redis_client = Redis()
        else:
            self.redis_client = redis_client

    def __repr__(self):
        return "<RedisModel(%s-%s)>" % (self.__prefix__, self.id)

    #@property
    #def id(self):
        #return self.attributes.get(self.id_attribute)

    @property
    def redis_key(self):
        """Get the redis key that store.
        """
        return self.__prefix__ + '-' + str(self.id)

    def fetch(self, **options):
        """Request the model's state from the redis server.
        """
        return self.set(self.unpack(self.redis_client.hgetall(self.redis_key)))

    def unpack(self, attributes):
        """unpack the value from redis
        """
        return dict(
            [(key, serializer.dumps(value)) for key, value in attributes.iteritems()]
        )

    def pack(self, attributes):
        """ pack the value before store to redis
        """
        return dict(
            [(key, serializer.loads(value)) for key, value in response.iteritems()]
        )

    def save(self, attributes=None, options=None):
        """Save a model to your redis-server
            @TODO: abilable options, {patch: True}
        """
        if attributes:
            self.set(attributes)
        value = self.pack(self.attributes)
        if value:
            return self.redis_client.hmset(self.redis_key, value)
        else:
            return None

    def destroy(self):
        """destroy from redis server for the current model.
        """
        return self.redis_client.delete(self.redis_key)

    def get(self, name):
        return self.attributes.get(name)

    def set(self, name, value=None, **kwargs):
        """
>>> model = RedisModel()
>>> model.set('key', 'value')
>>> model.set({'key': 'value'})
>>> model.set(key="value")
        """
        update_dict = {}
        if type(name) == DictType:
            update_dict.update(name)
        update_dict.update(kwargs)
        if type(name) in StringTypes and type(value) in StringTypes:
            update_dict.update({name: value})

        if self.id_attribute in update_dict:
            self.id = update_dict.get(self.id_attribute)

        return self.attributes.update(update_dict)

    def toJSON(self):
        return self.attributes


class RedisCollection(object):
    """
    """
    model = None
    models = None

    def __init__(self, models=None, **options):
        """ """
        self.models = [model for model in models if isinstance(models, RedisModel)]


if __name__ == '__main__':
    assert RedisModel(prefix='song', id='369918').__repr__() == \
        RedisModel({'id': 369918}, prefix='song').__repr__()

    rm = RedisModel({'id': 369918}, prefix='song')
    assert rm.toJSON() == {}

