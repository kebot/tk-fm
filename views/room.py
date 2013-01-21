#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from turkeyfm import app

def _create_song(sid):
    """ for test use
    """
    return {'id': sid, 'name': "song-%i" % sid}

class RoomNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    # messages shared between room
    nicknames = []

    def initialize(self):
        # @TODO a better logger
        self.logger = app.logger
        self.web_session = self.request
        self.current_song = _create_song(1)

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room):
        self.room = room
        self.join(room)
        self.emit('current_song', self.current_song)
        return True

    def on_nickname(self, nickname):
        self.log('Nickname: {0}'.format(nickname))
        self.nicknames.append(nickname)
        self.session['nickname'] = nickname
        self.broadcast_event('announcement', '%s has connected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        return True, nickname

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        nickname = self.session['nickname']
        self.nicknames.remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.emit_to_room(self.room, 'msg_to_room',
            self.session['nickname'], msg)
        return True


