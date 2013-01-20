#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import RedisModel

class User(RedisModel):
    __prefix__ = 'user'

