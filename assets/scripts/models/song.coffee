define [
  'models/io'
  'utils/time'
], (
  IOModel
  time
)->

  class Song extends IOModel
    idAttribute: 'sid'
    url: "/song/#{@id}"
    serialize: -> @toJSON()
    initialize: (attributes, options)->
      @set 'weight', time.current()


