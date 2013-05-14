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
from turkeyfm.models.room import Playlist, SongItem
from turkeyfm.models.redis_model import RedisModel

from turkeyfm.models.user import uid_from_session
from turkeyfm.models.song import is_like_the_song

import logging
logger = logging.getLogger('room')

class _RoomController(object):
    # for easy scaling, it will be use for routing.
    # for example: which instance should i use for the room xxxxx

    _instances = {}

    s_finish = -1
    s_unknow = 0
    s_playing = 1

    def __init__(self, rid):
        self.rid = rid
        self.current_song = SongItem()
        self.song_list = Playlist(id = rid)
        self.device_ns = set()
        self.ns_name = None
        logger.debug("Create global room: %s", rid)

    def get_init_data(self):
        return [dict(current_song=self.current_song.toJSON(),
                song_list=self.song_list.toJSON())]

    def nextsong(self):
        # actually skip the current_song
        # toggle to nextsong
        if not self.current_song.is_new():
            self.current_song.save({'finsh_play_time': time.time() * 1000})

        if self.song_list.length() > 0:
            logger.debug("room:{0}: nextsong".format(self.rid))
            next_song = self.song_list.shift()
            if next_song:
                self.current_song = next_song
                msg = self.current_song.toJSON()
                self.publish('current_song', msg)
                self.publish('songlist', {
                    'method': 'delete',
                    'data': {'sid': self.current_song.id}
                })
                for dev in self.device_ns:
                    dev.playing_status = self.s_unknow
        else:
            logger.debug('playlist is empty')

    def finish_playing(self, dev, **options):
        target_sid = options.get('sid')

        # it will always be skipped if serverside has nothing to play.
        if not self.current_song.id:
            logger.debug('no current_song set, nextsong.')
            return self.nextsong()

        if target_sid != self.current_song.id:
            logger.debug("Client current_song is %s, but in server is %s, skipped",
                    target_sid, self.current_song.id)
            return

        if dev.playing_status == self.s_finish:
            logger.debug("hey, you have reported you have finish song(%s), don't be harry.", target_sid)
            return

        dev.playing_status = self.s_finish
        list_status = [dev.playing_status for dev in self.device_ns if
                dev.playing_status != self.s_unknow]
        logger.debug(str(list_status))
        def can_skip(list_status):
            return 2 * list_status.count(self.s_finish) - len(list_status) >= 0

        if can_skip(list_status):
            return self.nextsong()
        pass

    def begin_playing(self, dev, msg):
        def pick(d, *keys):
            return dict({ (key, d.get(key)) for key in keys})

        try:
            msg = pick(msg, 'sid', 'report_time', 'position')
        except KeyError, e:
            logger.info('msg passing did not have all key: %s', msg)
            return

        dev.playing_status = self.s_playing
        if not self.current_song.get('report_time'):
            self.current_song.save(msg)
            self.publish('current_song', msg)
            pass

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
        self.web_session = self.request or {}

    # // sync time between client and server
    def on_ntp(self):
        return [time.time() * 1000]

    def on_join(self, room):
        # @TODO for test use, remove this two line
        #import uuid
        #room = str(uuid.uuid1())

        self.room = get_room(room)
        self.room.join(self)
        return self.room.get_init_data()

    def on_leave(self, *args):
        # args is not required currently(only one room pre client)
        if self.room:
            self.room.leave(self)
            self.room = None
        else:
            logger.info("Does not have join any room, can't leave.")
        return True

    def disconnect(self, silent=True):
        self.room.leave(self)
        return super(RoomNamespace, self).disconnect(silent)

    def revc_disconnect(self):
        return self.disconnect(silent=True)

    def on_songlist(self, msg):
        song_list = self.room.song_list
        #logger.debug(song_list.toJSON())
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
                return [True]
            else:
                model = song_list.create(msg.get('data'))
                logger.debug("Add <sid=%s> to song_list(%s)", str(model.id), str(song_list.toJSON()))
                msg['data'] = model.toJSON()
                self.room.publish(channel, msg)

                if self.room.current_song.is_new():
                    self.room.nextsong()
                #logger.debug(song_list.toJSON())
                return [True]

        elif method == 'DELETE':
            self.room.publish(channel, msg)
            return [song_list.remove(_id=_id)]


    def on_current_song(self, msg):

        uid = uid_from_session(self.web_session)

        method = msg.get('method').upper()
        data = msg.get('data')

        sid = data.get('sid', None)

        if sid != self.room.current_song.get('sid'):
            # hey man, current song of your message is outdated
            # you will be notify for change song!
            pass

        # currently, only post is supported
        if method != 'PATCH':
            return [True]

        if data.get('finish') == True:
            # hey man, i'm finish playing the song, please deal with me!
            #print "CurrentSong: finishplaying", msg
            logger.debug("c:finish: sid=%s", sid)
            self.room.finish_playing(self, sid=sid)
            return [True]

        if data.get('begin') == True:
            logger.debug('c:begin: sid=%s', str(data))
            self.room.begin_playing(self, data)
            return [True]

        song_dict = dict(self.room.current_song.toJSON(), like=is_like_the_song(
                uid=uid,
                sid=self.room.current_song.get('sid'),
            ))

        self.room.publish('current_song', song_dict)

