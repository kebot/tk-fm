#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import json

from store import RedisStore, RedisHashes
from config import STORE_PREFIX
RedisStore.PREFIX_KEY = STORE_PREFIX

###########################################################
import doubanfm

##########################################################
# Inspire by Backbone.Model
##########################################################
class BaseModel(object):

    redis_client = None

    def __init__(self, store_id, attributes={}):
        # set default instance values
        self.defaults = {}
        stored = RedisHashes.getall(store_id)
        if type(stored) == dict:
            stored.update(attributes)
        elif stored == None:
            stored = attributes
        else:
            raise Exception('get unsupported type %s', str(type(stored)))
        self.attributes = stored

    def save(self):
        return RedisHashes.save(self.store_id, self.attributes)

    def initialize(self):
        raise NotImplementedError

    def get(self, key):
        return self.attributes.get(key)

    def set(self, key, value):
        return self.attributes.set(key, value)

    def has(self, key):
        return self.attributes.haskey(key) and self.attributes.get(key)

    def unset(self, key):
        return self.attributes.__delattr__(key)

    def clear(self):
        # delete all attributes
        self.attributes = {}

    def toJSON(self):
        json.dumps(self.attributes)

    def clone(self):
        raise NotImplementedError

    @property
    def id(self):
        return self.id

    @property
    def idAttribute(self, value):
        pass


##################################################
class Song(Model):
    """docstring for Song"""
    def __init__(self, id_key, attributes={}):
        super(Song, self).__init__()
        self.id_key = id_key



import unittest
class ModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_description(self):
        pass


if __name__ == '__main__':
    unittest.main()

