#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @TODO integrate with framework's session object.
# @TODO Server.


from socketio.namespace import BaseNamespace
from socketio.server import SocketIOServer

class NotifyNamespace(BaseNamespace):
    def on_chat(self, msg):
        self.emit('chat', msg)

def socketio_sevice(request):
    socketio_message()


from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'


import gevent.wsgi
import gevent.monkey
import werkzeug.serving

from werkzeug.debug import DebuggedApplication

gevent.monkey.patch_all()

@werkzeug.serving.run_with_reloader
def run_server():
    app.debug = True
    wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    # wsgi_app = app.wsgi_app
    print 'listening to port 8080 and port 843 (Flash policy server) \
            with debugger'
    SocketIOServer(('0.0.0.0', 8080), wsgi_app,
            resource='socket.io', policy_server=True,
            policy_listener=('0.0.0.0', 10843)).serve_forever()

if __name__ == '__main__':
    run_server()

