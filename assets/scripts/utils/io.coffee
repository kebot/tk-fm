define [
  'socket.io'
], (io)->
  socket = io.connect '/room'
  socket.on 'connect', -> console.info 'io-connect'
  socket.on 'disconnect', -> console.info 'io-disconnect'
  # custom events, current_song changed
  socket

