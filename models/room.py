#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .redis_model import RedisModel
from .redis_collection import RedisCollection

from yafa.redisdb.types import RedisHash, RedisList

import logging

import uuid
import types

logger = logging.getLogger('room')

from .song import Song

class RedisPubsubMixin(object):
    """ this module defines some event passing for redis-based datatypes with pubsub
..
    class Song(RedisHash, RedisPubsubMixin):

        def on_change(self):
            pass

        def listen_all(self):
            channels = ['change']
            return [self.listen(cnl) for cnl in channels]

    """
    def listen(self, event, callback=None):
        if callback is None:
            callback = 'on-' + self.event

        if type(callback) in types.StringTypes:
            try:
                callback = self.__getattribute__(callback)
            except AttributeError:
                self.logger.error("%s is not a method of this class" % (callback))
                pass

        if callable(callback):
            channel_name = self.key + '-' + event
            # @TODO
            # where can i found the pubsub instance?
            pubsub.listen(channel_name, callback)
        else:
            self.logger.error("The callback is not callable:",  callback)
            return

        pass



class SongItem(RedisModel):
    """
.. attributes
        sid: <sid>
        creater: <uid> // who add this song to the playlist
        maintainer: <uid> // who is playing the song
        position: int
        begin_time: timestamp

other attributes for the song is copy from key="song-<sid>"
```
    """
    __prefix__ = 'room-currentsong'
    id_attribute = 'sid'

    extend_class = Song

    def toJSON(self, *args, **kwargs):
        song_attrs = Song(id=self.id).toJSON(fetch=True)
        extra_attrs = RedisModel.toJSON(self, *args, **kwargs)
        #logger.debug("SongItem->toJSON():self.id: {0} \n song_attrs: {1} \n extra_attrs: {2}".format(self.id, song_attrs, extra_attrs))
        song_attrs.update(extra_attrs)
        return song_attrs
    pass


class Playlist(RedisCollection):
    model_class = SongItem


class Room(RedisModel):
    """define store for room

        contain data-structures:
            `creater/admin`: the clients

        // Playlist: <redis_list>
        // playlist.key = 'playlist-<rid>'
        // playlist.append({ 'sid': 1111,  })

        room-onlineusers-<rid>: *redis set of online-users
        room-currentsong-<rid>: *redis-hash of current song
        room-currentplaylist: *redis-lists / redis-ordered-sets
    """
    __prefix__ = 'room'

    #@property
    #def current_song(self):
        #return CurrentSong(rid=self.id)

    #@property
    #def current_playlist(self):
        #return Playlist(rid=self.id)

    @classmethod
    def create(cls, creater):
        the_id = uuid.uuid1()
        attributes = dict(id=the_id, creater=creater)
        ins = cls(attributes)
        return ins

    #def current_song(self):
        # CurrentSong is a proxy to redis hash
        #pass


    @property
    def key_for_currsong(self):
        if self.id is not None:
            return self.__prefix__ + '-' + self.id
        return None

    @property
    def key_for_playlist(self):
        if self.id is not None:
            return self.__prefix__ + '-' + self.id
        return None



# - * - testcase for this module - * -

# room -> set CurrentSong, Auto Message for all Model and other data
# structures.

import unittest
import mock


class RoomTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_create(self):
        # Create a new room, with a random uuid
        on_currentsong_change = mock.MagicMock(name='whatever')
        room = Room.create(creater=247549)
        room.current_song.change()
        room.current_song.listen('change', on_currentsong_change)
        self.assertTrue(on_currentsong_change.called())
        # has a redis hash mixin, three hash

        pass

    def test_modify_room(self):
        # Patch 2 current_song
        room.current_song
        # common event: { 'method': 'patch', 'attributes': '' }

    def tearDown(self):
        pass

    pass

if __name__ == '__main__':
    unittest.main()

