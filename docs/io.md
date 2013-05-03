Flask-like router with socket.io
```python
        @app.route('/socket.io/<path:remaining>')
        def socketio(remaining):
            try:
                socketio_manage(request.environ, {'/room': SomeNamespace},
                        request=session_info)
            except:
                app.logger.error('Exception while')
        
        class RoomNamespace(object):
            def on_user_message(self, msg):
                # something
                # 
                # 

from flask.socketio import message

sio = FlaskSocketIO(endpoint='/socket.io')
ns = sio.namespace('/room')
@ns.route('currentsong')
def on_currentsong(message):
    # request, cookie is read only and may be outdated
    # server_side_session can be write

```


limit with request and session

    Can be changed with other 

Solutions:
    so I can private a event when this change happens.

http://flask.pocoo.org/docs/signals/



