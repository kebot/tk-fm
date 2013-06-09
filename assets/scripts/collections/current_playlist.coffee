define [
  'backbone'
  'utils/iosync'
  'utils/io'
], (
  Backbone
  iosync
  io
)->
  class Song extends Backbone.Model
    url: 'songlist'
    sync: iosync
    serialize: -> @toJSON()
    idAttribute: 'sid'

  class Playlist extends Backbone.Collection
    sync: iosync

    model: Song
    initialize: ->
      io.on 'songlist', (msg)=>
        if msg.method == 'create' or msg.method == 'put'
          @add msg.data
        else if msg.method == 'delete'
          @remove msg.data.sid
        else if msg.method == 'reset'
          @reset msg.data
    url: 'songlist'
    comparator: (song)->
      song.get('weight')

  new Playlist()

