#!/usr/bin/env python
# -*- coding: utf-8 -*-

from types import ListType
import redis

redis_server = redis.Redis('localhost')

class RedisStore():
    PREFIX_KEY = 'turkeyfm_'
    def __init__(self, key, prefix=None):
        self.key = key

class RedisString(RedisStore):
    """docstring for RedisString"""
    def __init__(self, key, value=""):
        super(RedisString, self).__init__(key)

class RedisHashes(RedisStore):
    """ map available redis interface for Hashes
    hdel : __delattr__
    hexists : hasattr
    hget : __getattr__, get
    hgetall : @TODO
    hincrby: @TODO, increment the integer value of a hash field by the given number
    hincrbyfloat: @TODO
    hkeys: keys
    hlen: __length__
    hmget: @TODO
    hset: __setattr__
    hsetnx: @TODO set the value only if the key is not exists
    hvals: values
    """
    @staticmethod
    def getall(key):
        return redis_server.hgetall(key)

    @staticmethod
    def save(key, value):
        return redis_server.hmset(key, value)

    def __init__(self, key, value={}):
        #super(RedisHashes, self).__init__(key)
        self.key = key
        self.update(value)

    def update(self, value):
        return redis_server.hmset(self.key, value)

    def set(self, key, value):
        return redis_server.hset(self.key, key, value)

    def get(self, key):
        return redis_server.hget(self.key, key)

    def keys(self):
        return redis_server.hkeys(self.key)

    def values(self):
        return redis_server.hvals(self.key)

    def __delattr__(self, key):
        return redis_server.hdel(self.key, key)

    def __setattr__(self, key, value):
        return self.set(key, value)

    def __getattr__(self, key):
        return self.get(key)

    def has_key(self, key):
        return redis_server.hexists(self.key, key)

    def __length__(self):
        return redis_server.hlen(self.key)


if __name__ == '__main__':
    # test RedisHashes
    h = RedisHashes('test_hashes', {'hello': 'world', 'keith': 'yao'})
    print h.keys()
    print h.values()

RedisDict = RedisHashes


class RedisList(object):
    """
        >>> jh = RedisList('default', ['hello', 'world', 'keith'])
        >>> jh
        <RedisList at key=default>
    """
    def __init__(self, key, values=[]):
        super(RedisList, self).__init__()
        self.initialize(key, values)

    def initialize(self, key, values):
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
        #index_value = redis_server.lindex(self.key, i)
        redis_server.lrem(self.key, x, 1)

    def pop(self, i=None):
        if not i:
            return redis_server.lpop(self.key)
        else:
            return redis_server.lrem(self.key, i)

    def index(self, x):
        pass

    def get(self, i):
        return redis_server.lindex(self.key, i)

    def __getitem__(self, i):
        if type(i) == slice:
            return self.__getsilence__(i.start, i.stop, i.step)
        return self.get(i)

    def __getsilence__(self, start=None, stop=None, step=None):
        if not start:
            start = 0
        if not stop:
            stop = self.__len__()

        return redis_server.lrange(self.key, start, stop)

    def __len__(self):
        return redis_server.llen(self.key)

    def __repr__(self):
        return "<RedisList at key=%s>" % self.key


#songlist = SongList(['first', 'second', 'third'])

if __name__ == '__main__':
    import doctest
    doctest.testmod()


