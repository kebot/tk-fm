#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
from song import Song
import uuid

class Playlist(list):
    id_attribute = 'sid'

    def __init__(self, items=None, key=None, **options):
        super(Playlist, self).__init__()
        # @TODO will be replace by RedisType instead
        #self.DictType = types.DictType
        #self.ListType = types.ListType
        self.key = key or str(uuid.uuid1())
        # infohash{'sid': {extra_info}}
        #self.infohash = self.DictType()
        if items:
            self.add(items)

    def get(self, sid):
        for i in self:
            if sid == i.get(self.id_attribute):
                return i

    def add(self, item):
        if self.get(item.get(self.id_attribute)):
            return False
        else:
            self.append(item)

