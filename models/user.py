#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel

class User(RedisModel):
    __prefix__ = 'user'

def uid_from_session(session_obj):
    return session_obj.get('user_info', {}).get('user_id')

