from socketio.server import SocketIOServer
from turkeyfm import app

if __name__ == '__main__':
    app.debug = True
    PORT = 5000
    print 'Listening on http://127.0.0.1:%s and on port 10843 (flash policy server)' % PORT
    SocketIOServer(('', PORT), app, resource="socket.io").serve_forever()

