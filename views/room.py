#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import types

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin

from yafa.redisdb import get_redis
from yafa.redisdb.types import RedisSet, RedisHash

from turkeyfm import app
from turkeyfm.models.song import UserSong
from .mixins import RedisPubsubMixin
from turkeyfm.models.room import Playlist, CurrentSong as ModelCurrentSong
from turkeyfm.models.redis_model import RedisModel

from turkeyfm.models.user import uid_from_session
from turkeyfm.models.song import is_like_the_song

import logging
logger = logging.getLogger('room')



"""
class CurrentSong(object):
    # device id / currentsong
    # relationship between currentsong / current device
    # "key=current_song_status-<rid>"
    #   { device_id: <status>, ...}

    def initialize(self, **options):
        self.device_id = options.get('device_id', None)

    # hash -> first play, first finish.
    def status_key(self):
        return self.__prefix__ + '-status'

    status_unknow = 0
    status_playing = 1
    status_waitting = -1 # waitting for loading, buffering, etc..
"""


class _RoomController(object):
    # for easy scaling, it will be use for routing.
    # for example: which instance should i use for the room xxxxx

    _instances = {}

    s_finish = -1
    s_unknow = 0
    s_playing = 1

    def __init__(self, rid):
        self.rid = rid
        self.current_song = ModelCurrentSong(id = rid)
        self.song_list = Playlist(id = rid)
        self.device_ns = set()
        self.ns_name = None

    def get_init_data(self):
        return [dict(current_song=self.current_song.toJSON(),
                song_list=self.song_list.toJSON())]

    def nextsong(self):
        # actually skip the current_song
        # toggle to nextsong
        if self.current_song.is_new():
            self.current_song.set('finsh_play_time', time.time() * 1000)

        if self.song_list.length() > 0:
            next_song = self.song_list.shift()
            if next_song:
                self.current_song = next_song
                self.publish('current_song', self.current_song.toJSON())
        else:
            logger.debug('playlist is empty')

    def finish_playing(self, dev):
        if self.current_song.id == None:
            logger.debug('no current_song set')
            return self.nextsong()
        else:
            dev.playing_status = self.s_finish
            list_status = [dev.playing_status for dev in self.device_ns if
                    dev.playing_status != self.s_unknow]
            def can_skip(list_status):
                return 2 * list_status.count(self.s_finish) - len(list_status) >= 0
            if can_skip(list_status):
                return self.nextsong()
        pass

    def begin_playing(self, dev):
        dev.playing_status = self.s_playing
        # who is reporter
        if not self.current_song.get('report_time'):
            pass
            #self.current_song.save({
            #})

    # room related methods
    def join(self, dev):
        #print "<rid-%s with %i devices>" % (self.rid, len(self.device_ns) + 1)
        if not self.ns_name:
            self.ns_name = dev.ns_name

        dev.playing_status = self.s_unknow

        return self.device_ns.add(dev)

    def leave(self, dev):
        #print "<rid-%s with %i devices>" % (self.rid, len(self.device_ns) - 1)
        return self.device_ns.remove(dev)

    def publish(self, event, *args, **options):
        """@todo: Docstring for post_message
        :event: event body
        :*args: argument of a event
        :**options: if except is given, the except sockets will be skipped.
        :returns: None
        """
        excepts = []
        if 'except' in options:
            if type(options.get('except')) is list:
                excepts = [options.get('except')]
            else:
                excepts = options.get('except')

        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)

        return [dev.socket.send_packet(pkt) for dev in self.device_ns
                if dev not in excepts]


def get_room(rid):
    ro_m = _RoomController._instances.get(rid)
    if not ro_m:
        ro_m = _RoomController(rid=rid)
        _RoomController._instances.__setitem__(rid, ro_m)
    return ro_m

# helper methods


class RoomNamespace(BaseNamespace):

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
        # @TODO for test use, remove this two line
        import uuid
        room = str(uuid.uuid1())

        self.room = get_room(room)
        self.room.join(self)
        return self.room.get_init_data()

    def disconnect(self, silent=True):
        self._leave_room()
        return super(RoomNamespace, self).disconnect(silent)

    def _leave_room(self):
        if self.room:
            self.room.leave(self)

    def revc_disconnect(self):
        return self._leave_room()

    def on_leave(self, room):
        return get_room(room).leave(self)

    def on_finish(self, msg):
        # // user finish playing `current_song`
        pass

    def on_songlist(self, msg):
        #print msg
        song_list = self.room.song_list
        data = msg.get('data')
        method = (msg.get('method') or 'get').upper()
        _id = song_list.get('_id')
        channel = 'songlist'

        # get untest
        if method == 'GET':
            if _id:
                return song_list.get(_id).toJSON()
            else:
                return song_list.toJSON()
        # post untest
        elif method in ['POST', 'PUT', 'PATCH']:
            model = song_list.get(_id)
            if model:
                #print "Model", model  ,"exists with id, ", model.id
                # "this is patch/put"
                # currently, modify will be skipped, not supported!
                return [True]
            else:
                #print '-------------------------------create one'
                model = song_list.create(msg.get('data'))
                msg['data'] = model.toJSON()
                self.room.publish(channel, msg)
                return [True]

        elif method == 'DELETE':
            self.room.publish(channel, msg)
            return [song_list.remove(_id=_id)]


    def on_current_song(self, msg):

        uid = uid_from_session(self.web_session)

        method = msg.get('method').upper()
        data = msg.get('data')

        if data.get('sid') != self.room.current_song.get('sid'):
            # hey man, current song of your message is outdated
            # you will be notify for change song!
            pass

        # currently, only post is supported
        if method != 'PATCH':
            return [True]

        if data.get('finish') == True:
            # hey man, i'm finish playing the song, please deal with me!
            self.room.finish_playing(self)
            return [True]

        if data.get('begin') == True:
            self.room.begin_playing(self)
            return [True]

        # data.get('sid') is current_song
        # self.room.current_song.save(attributes)

        song_dict = dict(self.room.current_song.toJSON(), like=is_like_the_song(
                uid=uid,
                sid=self.room.current_song.get('sid'),
            ))

        self.room.publish('current_song', song_dict)

    def recv_disconnect(self):
        self.log('Disconnected')
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        self.emit_to_room(self.room, 'msg_to_room',
            self.session['nickname'], msg)
        return True

