#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Monkey Patch
from gevent import monkey; monkey.patch_all()

import redis
import gevent

def listen_loop():
    client = redis.Redis()
    psub = client.pubsub()
    psub.subscribe('turkey')
    for msg in psub.listen():
        print msg

def publish():
    print 'Before publish'
    for i in xrange(10):
        print i
        gevent.sleep(1)
    client = redis.Redis()
    client.publish('turkey', 'a message')
    print 'After publish'

gevent.joinall([
    gevent.spawn(listen_loop),
    gevent.spawn(publish)
    ])


