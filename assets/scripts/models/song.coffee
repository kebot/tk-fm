define [
  'backbone'
  'utils/time'
], (
  Backbone
  time
)->
  # @TODO modify this to room-song idAttribute `id`: <roomid-sid>

  class Song extends Backbone.Model
    idAttribute: 'sid'
    url: "/song/#{@id}"
    serialize: -> @toJSON()
    initialize: (attributes, options)->
      @set 'weight', time.current()

