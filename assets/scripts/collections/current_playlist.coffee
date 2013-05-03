define [
  'collections/io'
  'backbone'
  'utils/iosync'
  'utils/io'
], (
  IOCollection
  Backbone
  iosync
  io
)->
  class Song extends Backbone.Model
    url: 'songlist'
    sync: iosync
    serialize: -> @toJSON()
    idAttribute: 'sid'

  class Playlist extends IOCollection
    model: Song
    initialize: ->
      io.on 'songlist', (msg)=>
        if msg.method == 'create'
          @add msg.data
        else if msg.method == 'delete'
          @remove @get(msg.data.sid)
        else if msg.method == 'reset'
          @reset msg.data
    url: 'songlist'
    comparator: (song)->
      song.get('weight')

  new Playlist()

