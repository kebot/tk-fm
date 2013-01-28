define [
  'models/io',
  'utils/io'
], (IOModel, io)->
  #io.on 'current_song', (msg)-> console.log msg

  class CurrentSong extends IOModel
    idAttribute: 'sid'
    url: -> 'current_song'
    # // attribudes not given
    initialize: ->
      io.on 'current_song', (msg)=>
        console.log 'Receive current_song from server!!!', msg
        @set msg

  return new CurrentSong()

