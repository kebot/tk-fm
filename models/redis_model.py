#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A storage in redis.

ps: in 2012, I begins writing this code. Now it's 2013! Happy New Year!
"""

from types import DictType, StringTypes
from flask import g, json as serializer
from yafa.redisdb import get_redis as get_redis_client
import uuid


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

        if 'collection' in options:
            self.collection = options['collection']
        else:
            self.collection = None

        if not hasattr(self, '__prefix__'):
            if 'prefix' in options:
                self.__prefix__ = options.get('prefix')
            else:
                self.__prefix__ = self.__class__.__name__

        if not redis_client:
            self.redis_client = get_redis_client()
        else:
            self.redis_client = redis_client

    def __repr__(self):
        return "<RedisModel(key=%s)>" % (self.redis_key)

    @property
    def redis_key(self):
        """Get the redis key that store.
        """
        prefix = self.__prefix__
        if self.collection:
            prefix += '-' + str(self.collection.id)
        return prefix + '-' + str(self.id)

    def is_new(self):
        """ check the redis model exists in redis server. """
        return not self.redis_client.exists(self.redis_key)

    def fetch(self, **options):
        """Request the model's state from the redis server.
        """
        return self.set(self.unpack(self.redis_client.hgetall(self.redis_key)))

    def unpack(self, attributes):
        """unpack the value from redis
        """
        #print "Model: Unpack", attributes
        def loads(value):
            value_type = type(value)
            if type(value) == DictType:
                return value
            try:
                return serializer.loads(value)
            except ValueError, e:
                if value_type in StringTypes:
                    return value
                else:
                    raise e

        return dict(
            [(key, loads(value)) for key, value in attributes.iteritems()]
        )

    def pack(self, attributes):
        """ pack the value before store to redis
        """
        def dumps(value):
            if type(value) == DictType:
                return serializer.dumps(value)
            return value

        return dict(
            [(key, dumps(value)) for key, value in attributes.iteritems()]
        )

    def _random_id(self):
        return str(uuid.uuid1())

    def save(self, attributes=None, options=None):
        """Save a model to your redis-server.
        If attribute is given, only the given attributes will be save.

            @todo: add a changed hash
            @todo: abilable options, {patch: True}
        """
        if attributes:
            self.set(attributes)
        else:
            attributes = self.attributes
        # the item is new, and not yet have a id attribute, will in create function
        #if self.id_attribute not in attributes:
            #self.set(self.id_attribute, self._random_id())
        value = self.pack(attributes)
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
        if type(name) == DictType:
            update_dict = name
        else:
            update_dict = {}

        if kwargs:
            update_dict.update(kwargs)

        if type(name) in StringTypes and type(value) in StringTypes:
            update_dict.update({name: value})

        if self.id_attribute in update_dict:
            self.id = update_dict.get(self.id_attribute)

        return self.attributes.update(update_dict)

    def toJSON(self, **kwargs):
        if kwargs.get('fetch', None) or self.attributes == {}:
            #print 'RedisModel: Fetch model with key', self.redis_key
            self.fetch()
        return self.attributes


if __name__ == '__main__':
    assert RedisModel(prefix='song', id='369918').__repr__() == \
        RedisModel({'id': 369918}, prefix='song').__repr__()

    rm = RedisModel({'id': 369918}, prefix='song')
    assert rm.toJSON() == {}




