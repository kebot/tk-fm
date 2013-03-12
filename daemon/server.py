#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turkeyfm.daemon.manager import Manager
from turkeyfm.daemon.worker import FavSongWorker

def run_server():
    import threading
    make = Manager()
    make.add_worker(FavSongWorker)
    threading.Thread(target=make.love).start()

if __name__ == '__main__':
    run_server()

