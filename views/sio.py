#!/usr/bin/env python
# -*- coding: utf-8 -*-
from turkeyfm import app
from flask import request, session, Response
from socketio import socketio_manage

from .room import RoomNamespace

@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        session_info = dict(session)
        socketio_manage(request.environ, {'/room': RoomNamespace},
                request=session_info)
    except:
        app.logger.error("Exception while handling socketio connection")

    return Response()


