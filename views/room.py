#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from turkeyfm import app
from turkeyfm import models

current_song = {}
song_list = []

class RoomNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def initialize(self):
        # @TODO a better logger
        self.logger = app.logger
        self.web_session = self.request
        self.current_song = current_song

    def emit_song_list(self):
        def build_song(sid):
            m = models.Song(id=sid)
            m.fetch()
            return m.toJSON()
        data = [build_song(sid) for sid in song_list]
        self.emit('songlist', { 'method': 'reset', 'data': data })

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def error(self, message):
        self.logger.error("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room):
        self.log('someone join the room')
        self.room = room
        self.join(room)
        self.emit('current_song', self.current_song)
        self.emit_song_list()
        return True

    def on_songlist(self, msg):
        method = msg.get('method')
        data = msg.get('data')
        if method == 'read':
            return True, song_list
        elif method == 'create' or method == 'update':
            # @TODO exists sid
            index = data.get('index', None)
            sid = data.get('sid')
            if sid in song_list:
                return True, 'Song alread exists'
            if index:
                song_list.insert(index, sid)
            else:
                song_list.append(sid)
                data['index'] = song_list.index(sid)
            #msg['creater'] = self.session
            self.log('emit_msg_to_room')
            self.emit_to_room(self.room, 'songlist', msg)
            return False, data
        elif method == 'remove':
            sid = data.get('sid')
            try:
                song_list.remove(sid)
            except ValueError:
                self.error("%i is not in songlist" % sid)
            return False
        else:
            return True, {}

    def on_current_song(self, msg):
        method = msg.get('method')
        self.current_song.update(msg.get('data'))
        self.emit_to_room(self.room, 'current_song', self.current_song)

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.emit_to_room(self.room, 'msg_to_room',
            self.session['nickname'], msg)
        return True


