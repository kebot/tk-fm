define [
  'socket.io'
  'models/current_user'
], (io, current_user)->
  ns = io.connect '/room'
  ns.on 'connect', ->
    console.info 'io-connect'
    current_user.set('sessionid', ns.socket.sessionid)
  ns.on 'disconnect', -> console.info 'io-disconnect'
  return ns

