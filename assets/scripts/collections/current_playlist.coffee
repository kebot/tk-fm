define [
  'collections/io',
  'models/io',
  'utils/io'
], (IOCollection, IOModel, io)->
  class Song extends IOModel
    url: 'songlist'
    idAttribute: 'sid'

  class Playlist extends IOCollection
    model: Song
    initialize: ->
      io.on 'songlist', (msg)=>
        if msg.method == 'create'
          this.add msg.data
        else if msg.method == 'remove'
          this.remove msg.data
        else if msg.method == 'reset'
          this.reset msg.data

  new Playlist()

