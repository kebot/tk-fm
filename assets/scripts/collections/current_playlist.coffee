define [
  'collections/io',
  'models/song',
  'utils/io'
], (IOCollection, IOSong, io)->

  class Song extends IOSong
    url: 'songlist'

  class Playlist extends IOCollection
    model: Song
    initialize: ->
      io.on 'songlist', (msg)=>
        if msg.method == 'create'
          @add msg.data
        else if msg.method == 'remove'
          @remove @get(msg.data.sid)
        else if msg.method == 'reset'
          @reset msg.data

    comparator: (song)->
      song.get('weight')

  new Playlist()

