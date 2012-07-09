#!/usr/bin/env python
# -*- coding: utf-8 -*-
import underscore as _
from types import ListType

import redis

redis_server = redis.Redis('localhost')

class RedisList():
    """
        >>> jh = RedisList('default', ['hello', 'world', 'keith'])
        >>> print jh
    """
    def __init__(self, key, values=[]):
        self.key = key
        if values:
            redis_server.delete(self.key)
            self.extend(values)

    def append(self, x):
        redis_server.rpush(self.key, x)

    def extend(self, l):
        _.each(l, self.append)

    def insert(self, i, x):
        # 2 steps
        redis_server.linsert(self.key, 'after', self.get(i), x)

    def remove(self, x):
        # 
        index_value = redis_server.lindex(self.key, i)

    def pop(self, i=None):
        if not i:
            return redis_server.lpop(self.key)
        else:
            return redis_server.lrem(self.key, i)

    def index(self, x):
        pass

    def get(self, i):
        return redis_server.lindex(self.key, i)

    def __len__(self):
        return redis_server.llen(self.key)

    def __repr__(self):
        return "<RedisList at key=%s>" % self.key


class SongList(RedisList):
    """
        >>> myloft = SongList(['hello', 'world', 'keith', 'yao'])
        >>> myloft.ding('yao')
        >>> print myloft
        ['yao', 'hello', 'world', 'keith']
    """
    def __init__(self, key, values):
        super(SongList, self).__init__(key, values)

    def shuffle(self):
        self = _.shuffle(self)
        return self

    def ding(self, song):
        self.insert(0, self.pop(self.index(song)))


songlist = SongList(['first', 'second', 'third'])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
