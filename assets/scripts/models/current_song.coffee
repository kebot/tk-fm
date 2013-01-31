define [
  'models/io',
  'utils/io'
  'underscore'
], (IOModel, io, _)->
  #io.on 'current_song', (msg)-> console.log msg

  class CurrentSong extends IOModel
    idAttribute: 'sid'
    url: -> 'current_song'
    # // attribudes not given
    initialize: ->
      io.on 'current_song', (msg)=>
        console.log 'Receive current_song from server!!!', msg

        # if song-changed, clear previous attributes(player position,
        #     begin time...)
        if not _.isUndefined(msg[@idAttribute]) and msg[@idAttribute] != @id
          @clear silent: true
        @set msg

  return new CurrentSong()

