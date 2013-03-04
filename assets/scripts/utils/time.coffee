# usage: server_current_time = require('utils/time').current()

define [
  'finish'
  'moment',
  'utils/io'
], (finish, moment, io)->

  ntp_sync = ->
    begin_time = moment.utc().valueOf()
    io.emit 'ntp', (server_time)->
      end_time = moment.utc().valueOf()
      server_current_time = server_time + (end_time - begin_time) / 2
      time_offset = end_time - server_current_time
      # local: 20 - server: 10 = 10
      # local: 30 - server: 30 -10 = 20
      finish(
          offset: time_offset
          current: -> moment.utc().valueOf() - time_offset
      )

  if io.socket.connected
    ntp_sync()
  else
    io.on 'connect', ntp_sync

