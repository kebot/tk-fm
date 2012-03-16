#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import json

class Client(redis.Redis):
    """docstring for Client"""
    def __init__(self, *arga, **argd):
        super(Client, self).__init__(*arga, **argd)

    def setDict(self, key, value):
        return self.set(key, json.dumps(value))

    def getDict(self, key):
        value = self.get(key)
        if value:
            return json.loads(value)
        else:
            return None


store = Client()
