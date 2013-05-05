#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()

import timeit
from yafa.redisdb.types import RedisHash, RedisList

from turkeyfm.models.redis_model import RedisModel
import uuid

"""
    `key`: room-songlist-<rid>: [1, 2, 3, 4, 5]
    `item_class`: whatever

    available redis datastructures:
        hash - {}
        list - []
        set  - set()

"""

class RedisCollection(object):
    # List Based
    model_class = RedisModel
    __prefix__ = ""

    def __init__(self, **options):
        """docstring for __init__"""
        if 'id' in options:
            self.id = options['id']
        else:
            self.id = self.generate_id()

        self.models = RedisList(key=self.key)
        self.initialize(**options)

    def initialize(self, **options):
        pass

    def generate_id(self):
        return str(uuid.uuid1())

    @property
    def key(self):
        return self.__prefix__ + "-" + str(self.id)

    def at(self, index):
        """ get a model from a collection, specified by index """
        return self.get(self.models[index])

    def get(self, i):
        """ get model from a collection, specified by an `id` """
        return self.model_class(id=i)

    def remove(self, model=None, _id=None, index=None):
        if model is not None and isinstance(model, self.model_class):
            pass
        elif _id:
            model = self.get(_id)
        elif index:
            model = self.get(index)
        else:
            raise Exception("a model, _id or model or index in model is required")
        if not model:
            # no model found!
            return False

        model.destroy()
        return self.models.remove(model.id)


    def toJSON(self):
        return [self.model_class(id=i).toJSON(fetch=True) for i in
                self.models]
                #self.models.all()]

    def create(self, attributes, **options):
        model = self.model_class(attributes)
        # @TODO handle create error problem.
        model.save()
        self.models.append(model.id)
        return model

    def length(self):
        return self.models.length()

    def __iter__(self):
        for key in self.models:
            yield self.model(key=key)


if __name__ == '__main__':
    # @TODO more fast version, current score 0.59132194519 (slow enough)
    # 100 = 67.1843070984
    # 100 = 59.7349610329
    # not improving much, ignore it, maybe need a connection pool or
    import timeit
    def test():
        key = str(uuid.uuid1())
        coll = RedisCollection(key='redis-collection' + key)
        # add elements to the collection
        for i in xrange(1, 100):
            attributes = dict(value=str(uuid.uuid4()))
            coll.create(attributes)

        print coll.models.length()
        print coll.toJSON()

    print timeit.timeit(test, number=100)

