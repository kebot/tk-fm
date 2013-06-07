#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turkeyfm.views.room import RoomNamespace, get_room

import mock
import unittest

class TestRoomView(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        def create_room(i):
            request = None
            ns_name = 'room'
            environ = {
                'socketio': mock.Mock()
            }
            return RoomNamespace(environ, ns_name, request=None)

        self.rooms = [create_room(i) for i in xrange(0, 100)]
        pass


    def testJoinLeave(self):
        room_name = '412'
        members = [1, 2, 3, 4]
        for i in members:
            self.rooms[i].on_join(room_name)
        room = get_room(room_name)
        self.assertEqual(len(room.device_ns), len(members))
        self.rooms[i]


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()




