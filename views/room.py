#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import types

import logging
logger = logging.getLogger('room')

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin

from yafa.redisdb import get_redis
from yafa.redisdb.types import RedisSet

from turkeyfm import app
from turkeyfm.models.song import UserSong
from .mixins import RedisPubsubMixin
from turkeyfm.models.room import CurrentSong, Playlist


class RoomStore(object):
    def __init__(self, rid):
        self.devices = RedisSet(key='room-devices-' + str(rid))
        self.current_song = CurrentSong(id=rid)
        self.song_list = CurrentSong(id=rid)

    _instances = {}
    @staticmethod
    def get(rid):
        result = RoomStore._instances.get('rid')
        if not result:
            result = RoomStore(rid)
        return result

    def join(self, device_id):
        self.devices.add(device_id)

    def leave(self, device_id):
        self.devices.remove(device_id)


class RoomNamespace(BaseNamespace, RoomsMixin):

    def initialize(self):
        # Support a better logger
        self.logger = app.logger
        self.web_session = self.request or {}

    # // helper methods
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def error(self, message):
        self.logger.error("[{0}] {1}".format(self.socket.sessid, message))

    # // sync time between client and server
    def on_ntp(self):
        return [time.time() * 1000]

    def on_join(self, room):
        self.log('someone join the room')
        self.room = room
        assert type(room) in types.StringTypes
        self.join(room)

        self.current_song = CurrentSong(id = room)
        self.song_list = Playlist(id = room)

        init_data = dict(current_song=self.current_song.toJSON(),
                song_list=self.song_list.toJSON())
        return [init_data]


    def on_finish(self, msg):
        # // user finish playing `current_song`
        # // 

        pass

    def publish(self, event, msg):
        return self.emit_to_room(self.room, event, msg)

    def on_songlist(self, msg):
        data = msg.get('data')
        method = (msg.get('method') or 'get').upper()
        _id = self.song_list.get('_id')

        channel = 'songlist'

        # get untest
        if method == 'GET':
            if _id:
                return self.song_list.get(_id).toJSON()
            else:
                return self.song_list.toJSON()
        # post untest
        elif method == 'POST':
            model = self.song_list.create(msg.get('data'))
            msg['data'] = model.toJSON()
            self.publish(channel, msg)
            return [True, model.toJSON()]
        elif method == 'PATCH' or method == 'PUT':
            model = self.song_list.get(data)
            attributes = msg['data']
            model.set(attributes)
            msg['data'] = model.toJSON()
            self.publish(channel, msg)
            return [True, msg['data']]
        elif method == 'DELETE':
            self.publish(channel, msg)
            return self.song_list.remove(_id=_id)


    def _on_songlist(self, msg):
        method = msg.get('method')
        data = msg.get('data')
        if method == 'read':
            return True, self.song_list
        elif method == 'create' or method == 'update':
            exist_song = self.song_list.get(data.get('sid'))
            if exist_song:
                exist_song.update(data)
            else:
                self.song_list.add(data)
            #self.log(self.song_list)
            self.emit_to_room(self.room, 'songlist', msg)
            return False, data
        elif method == 'delete' or method == 'remove':
            sid = data.get('sid')
            try:
                self.song_list.remove(self.song_list.get(sid))
                self.emit_to_room(self.room, 'songlist', msg)
            except ValueError:
                self.error("%i is not in songlist" % sid)
            return [False]
        else:
            return True, {}


    def on_current_song(self, msg):
        def is_like(sid):
            is_like = False
            info = self.web_session.get('user_info', None)
            if info:
                uid = info.get('user_id')
                if uid:
                    user_song = UserSong(uid)
                    is_like = user_song.get(sid)
            return is_like

        method = msg.get('method')
        data = msg.get('data')

        if data.get('sid') != self.current_song.get('sid'):
            #self.current_song.clear()
            self.current_song.destroy()

        attributes = msg.get('data')
        self.current_song.save(attributes)
        song_dict = dict(self.current_song.toJSON(), like=is_like(self.current_song.get('sid')))
        self.publish('current_song', song_dict)

    def recv_disconnect(self):
        self.log('Disconnected')
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.emit_to_room(self.room, 'msg_to_room',
            self.session['nickname'], msg)
        return True

