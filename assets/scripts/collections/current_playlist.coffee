define [
  'collections/io',
  'models/io',
  'utils/io'
], (IOCollection, IOModel, io)->
  class Song extends IOModel
    url: 'songlist'
    idAttribute: 'sid'
    serialize: -> @toJSON()

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

  new Playlist()

