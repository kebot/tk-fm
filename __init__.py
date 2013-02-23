#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import flask

app = flask.Flask(__name__)

from yafa.session import init_redis_session

app = init_redis_session(app)

# Configure for socket.io
import views

