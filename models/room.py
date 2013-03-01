#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel

# RedisSet
class FieldMixin(object):
    def __init__(self):
        pass
        #raise NotImplementedError('')


class Room(RedisModel):
    __prefix__ = 'room'
    gmt_create = NumberField()
    gmt_update = DateField()


