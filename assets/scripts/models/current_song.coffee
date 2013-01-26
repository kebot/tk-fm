define [
  'models/io',
  'utils/io'
], (IOModel, io)->
  io.on 'current_song', (msg)-> console.log msg

  class CurrentSong extends IOModel
    url: -> 'current_song'
    # // attribudes not given

  return new CurrentSong()

