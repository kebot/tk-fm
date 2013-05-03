#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent
if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()

import types
import gevent

from flask import json
serializer = json

# shared pubsub instance
from yafa.redisdb.pubsub import PubSub
from yafa.redisdb import get_redis
redis = get_redis()
pubsub = PubSub(redis.pubsub())
pubsub.start()

from turkeyfm.models.room import Room as RoomModel

class RedisPubsubMixin(object):
    """docstring for RedisPubsubMixin
        Call on disconnect.

        `recv_disconnect`

    """
    __prefix__ = 'room_'

    def __init__(self, *args, **kwargs):
        super(RedisPubsubMixin, self).__init__(*args, **kwargs)

    @property
    def channel_name(self):
        return self.__prefix__ + self.id

    def _subscribe_cb(self, msg):
        if type(msg) in types.StringTypes:
            msg = serializer.loads(msg)

        if type(msg) is types.DictionaryType:
            if 'except' in msg and self.socket.sessid in msg.get('except'):
                self.logger.debug('msg receive, but me is the senter, pass')
                return

            pkt = dict(type="event",
                       name=msg.name,
                       args=msg.args,
                       endpoint=self.ns_name)

            socket.send_packet(pkt)
            self.logger.debug('packet sented', pkt)
        else:
            self.logger.warning('Received message, but unknow type', msg)
        pass

    def join(self, room_id):
        self.id = room_id
        pubsub.listen(self.channel_name, self._subscribe_cb)
        pass

    def leave(self):
        pubsub.unlisten(self.channel_name, _subscribe_cb)
        pass

    def emit_to_room(self, room, event, *args, **options):
        # @TODO now One Socket can only join one room, it's true.
        ### by default, the message will be sent to all clients in this room!
        # just publish a message to a special redis channel
        msg = dict(
                options,
                name=event,
                args=args,
            )
        return redis.publish(self.channel_name, serializer.dumps(msg))

    pass


if __name__ == '__main__':
    import uuid
    room_name = str(uuid.uuid1())
    class TestNS(RedisPubsubMixin):
        pass

    view = TestNS()
    view.join(room_name)
    # publish to the Room
    view.emit_to_room('default_room', 'publish', {'msg': 'is here'})



