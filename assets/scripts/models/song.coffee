define [
  'models/io'
  'utils/time'
], (
  IOModel
  time
)->
  # @TODO modify this to room-song idAttribute `id`: <roomid-sid>

  class Song extends IOModel
    idAttribute: 'sid'
    url: "/song/#{@id}"
    serialize: -> @toJSON()
    initialize: (attributes, options)->
      @set 'weight', time.current()

