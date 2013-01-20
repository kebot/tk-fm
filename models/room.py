#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel

class Room(RedisModel):
    __prefix__ = 'room'


