#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from turkeyfm import app
from turkeyfm import models

g_current_song = {}
g_song_list = models.Playlist()

class RoomNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def initialize(self):
        # @TODO a better logger
        self.logger = app.logger
        self.web_session = self.request
        # @TODO create model for current_song
        print g_current_song
        print g_song_list
        self.current_song = g_current_song
        self.song_list = g_song_list #models.Playlist()

    def _get_song_list(self):
        return [song for song in self.song_list]

    def emit_song_list(self):
        self.emit('songlist', { 'method': 'reset', 'data':
            self._get_song_list() })

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def error(self, message):
        self.logger.error("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room):
        self.log('someone join the room')
        self.room = room
        self.join(room)
        print room
        init_data = dict(current_song=self.current_song,
                song_list=self._get_song_list())
        return [init_data]

    def on_songlist(self, msg):
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
        #elif method == 'update':
            #exist_song = self.song_list.get(data.get('sid'))
            #if not exist_song:
                #return True, 'The song does not exists in songlist'
            #exist_song.update(data)
            #self.log('emit_msg_to_room')
            #self.emit_to_room(self.room, 'songlist', msg)
            #return False, data
        elif method == 'remove':
            sid = data.get('sid')
            try:
                self.song_list.remove(self.song_list.get(sid))
            except ValueError:
                self.error("%i is not in songlist" % sid)
            return False
        else:
            return True, {}

    def on_current_song(self, msg):
        method = msg.get('method')
        data = msg.get('data')
        if data.get('sid') != self.current_song.get('sid'):
            self.current_song.clear()
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


