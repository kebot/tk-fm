#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   __  /_   _  ___
#   (  /) . /- / / )
#

"""
tk.fm - music in the sky
~~~~~~~~~~~~~~~~~~~~~~~~

"""
from gevent import monkey; monkey.patch_all()

# Config logging module
import logging
logging.basicConfig(format="%(message)s ,line %(lineno)d, %(pathname)s")

import flask
app = flask.Flask(__name__)
from turkeyfm.utils.session import init_redis_session
app = init_redis_session(app)
import views

# start the daemon
#from daemon import server
#server.run_server()

